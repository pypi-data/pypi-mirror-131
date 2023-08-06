import os
import json
import uuid
import hashlib
import base64
import time
import traceback

from typing import List

from azure.storage.queue import QueueClient
from azure.storage.blob import BlobClient
from azure.cosmosdb.table import TableService, TableBatch
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from .common import TaskResult, TaskMetadata, chunks

enough_workers_message = "There are already enough active workers"
workers_long_running = "Workers are active for too long. Going to process as well."
unhandled_exception_message = "Unhandled exception is appeared."

MAX_PROP_SIZE = 30000


class BlobReader:
    input_container = "input"
    output_container = "output"

    def __init__(self, connection_string, return_only_source):
        self.return_only_source = return_only_source
        self.connection_string = connection_string

    def read_blob_by_segments(self, blob_name: str):
        blob = self.get_input_blob(blob_name)
        blob_data = blob.download_blob()
        last_piece = ""
        for chunk in blob_data.chunks():
            lines = [l.strip() for l in chunk.decode().splitlines() if len(l.strip()) > 0]
            lines[0] = last_piece + lines[0]
            last_piece = lines[-1]
            for l in lines[:-1]:
                l = self._preprocess(l)
                if len(l) == 0:
                    continue
                source, target = json.loads(l)
                if self.return_only_source:
                    yield self._preprocess(source)
                else:
                    yield self._preprocess(source), self._preprocess(target)

        last_piece = self._preprocess(last_piece)
        if len(last_piece) > 0:
            source, target = json.loads(last_piece)
            if self.return_only_source:
                yield self._preprocess(source)
            else:
                yield self._preprocess(source), self._preprocess(target)

    def read_input_blob(self, blob_name):
        blob = self.get_input_blob(blob_name)
        return blob.download_blob().readall().decode()

    def read_output_blob(self, blob_name):
        blob = self.get_output_blob(blob_name)
        return blob.download_blob().readall().decode()

    def upload_output_blob(self, blob_name, content):
        out_blob = self.get_output_blob(blob_name)
        out_blob.upload_blob(content, timeout=1200, overwrite=True)

    def upload_input_blob(self, blob_name, content):
        in_blob = self.get_input_blob(blob_name)
        in_blob.upload_blob(content, timeout=1200, overwrite=True)
    
    def get_input_blob(self, blob_name):
        return BlobClient.from_connection_string(self.connection_string, container_name=self.input_container, blob_name=blob_name)

    def get_output_blob(self, blob_name):
        return BlobClient.from_connection_string(self.connection_string, container_name=self.output_container, blob_name=blob_name)

    @staticmethod
    def _preprocess(text):
        return text.replace("\xa0", " ").replace("&nbsp;", " ").strip()


class IdGenerator:
    @staticmethod
    def generate_request_id(data, worker_name, guid=None):
        if not guid:
            guid = IdGenerator.generate_id()
        data_to_hash = data + worker_name
        request_hash = str(hashlib.md5(data_to_hash.encode()).hexdigest())
        request_id = "%s_%s" % (guid, request_hash)
        return guid, request_hash, request_id

    @staticmethod
    def generate_id():
        return str(uuid.uuid4()).replace("-", "")
    
    @staticmethod
    def decode_id(request_id):
        guid, request_hash = request_id.split("_")
        return guid, request_hash


class MetadataRepository:
    failure_table = "executionFailures"
    segment_failure_table = "segmentExecutionFailures"

    def __init__(self, connection_string, metadata_table_name, create_if_not_exist = False):
        self.connection_string = connection_string
        self.metadata_table_name = metadata_table_name
        self.table_client = TableService(connection_string=self.connection_string)
        if create_if_not_exist:
            try:
                self.table_client.create_table(self.metadata_table_name)
            except ResourceExistsError:
                pass

    def set_task_error(self, pk, rk, error_message, stack_trace):
        entity = {"PartitionKey": pk, "RowKey": rk, "Error": error_message, "StackTrace": stack_trace }
        self.table_client.merge_entity(self.metadata_table_name, entity)

    def update_metadata(self, metadata: TaskMetadata):
        entity = metadata.to_dict()
        self.table_client.update_entity(self.metadata_table_name, entity)

    def insert_failure_record(self, worker_name, request_id, exception, stack_trace):
        failure_entity = {
            "PartitionKey": worker_name, 
            "RowKey": request_id, 
            "FailureMessage": exception, 
            "StackTrace": stack_trace
        }
        self.table_client.insert_or_replace_entity(self.failure_table, failure_entity)

    def exists(self) -> bool:
        return self.table_client.exists(self.metadata_table_name)

    def record_failure(self, request_id, e: Exception, worker_name):
        trace = traceback.format_exc()[:MAX_PROP_SIZE]
        error = str(e)[:MAX_PROP_SIZE]
        entity = {"PartitionKey": worker_name, "RowKey": request_id, "FailureMessage": error, "StackTrace": trace}
        self.table_client.insert_or_replace_entity(self.failure_table, entity)

    def record_segment_failures(self, request_id, worker_name, failures):
        batch, count = TableBatch(), 0
        for start, end, reason in failures:
            reason = reason[:MAX_PROP_SIZE]
            entity = {"PartitionKey": "%s_%s" % (worker_name, request_id), "RowKey": "%d_%d" % (start, end), "FailureMessage": reason, "Start": start, "End": end}
            batch.insert_or_replace_entity( entity)
            count += 1
            if count == 99:
                self.table_client.commit_batch(self.segment_failure_table, batch)
                batch = TableBatch()
        if count > 0:
            self.table_client.commit_batch(self.segment_failure_table, batch)

    def record_request_failure(self, metadata: TaskMetadata, e: Exception):
        trace = traceback.format_exc()
        error_message = str(e)
        entity = metadata.get_base_entity()
        entity["StackTrace"] = trace[:MAX_PROP_SIZE]
        entity["Error"] = error_message[:MAX_PROP_SIZE]
        self.table_client.merge_entity(self.metadata_table_name, entity)

    def insert_raw_metadata(self, data: List[str], params) -> str:
        entity = {"Data": data, "Params": params}
        serialized_body = json.dumps(entity)
        guid, request_hash, request_id = IdGenerator.generate_request_id(serialized_body, worker_name=self.metadata_table_name)
        metadata = {"PartitionKey": guid, "RowKey": request_hash, "Request": serialized_body }
        self.table_client.insert_entity(self.metadata_table_name, metadata)
        return request_id

    def insert_blobs_metadata(self, blob_names: List[str], params, guid) -> List[str]:
        request_ids = []
        if params is not None:
            params = json.dumps(params)
        for blobs_chunk in chunks(blob_names, 99):
            batch = TableBatch()
            for blob_name in blobs_chunk:
                guid, request_hash, request_id = IdGenerator.generate_request_id(blob_name, worker_name=self.metadata_table_name, guid=guid)
                batch.insert_or_replace_entity({"PartitionKey": guid, "RowKey": request_hash, "BlobName": blob_name, "Params": params})
                request_ids.append(request_id)
            self.table_client.commit_batch(self.metadata_table_name, batch)
        return request_ids

    def insert_blob_metadata(self, blob_name, params=None, guid=None) -> str:
        guid, request_hash, request_id = IdGenerator.generate_request_id(blob_name, worker_name=self.metadata_table_name, guid=guid)
        metadata_entity = {"PartitionKey": guid, "RowKey": request_hash, "BlobName": blob_name}
        if params:
            metadata_entity['Params'] = json.dumps(params)
        self.table_client.insert_entity(self.metadata_table_name, metadata_entity)
        return request_id

    def get_result_entity(self, request_id) -> TaskResult:
        pk, rk = IdGenerator.decode_id(request_id)
        entity = self.table_client.get_entity(self.metadata_table_name, pk, rk, select="PartitionKey,RowKey,Result,Error,StackTrace,State,Offset")
        return TaskResult.create_from_request_entity(entity)

    def get_result_entities(self, guid) -> List[TaskResult]:
        entities = self.table_client.query_entities(
            self.metadata_table_name, 
            filter="PartitionKey eq '%s'" % guid, 
            select="PartitionKey,RowKey,Result,Error,StackTrace,State,Offset"
        )
        return [TaskResult.create_from_request_entity(e) for e in entities]

    def get_task_metadata(self, request_id: str) -> TaskMetadata:
        guid, request_hash = IdGenerator.decode_id(request_id)
        entity = self.table_client.get_entity(self.metadata_table_name, guid, request_hash)
        return TaskMetadata.create_from_dict(entity)


class MessageQueueClient:
    def __init__(self, request_queue_name, poison_queue_name, connection_string, create_if_not_exist = False):
        self.queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=request_queue_name)
        self.poison_queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=poison_queue_name)
        if create_if_not_exist:
            try:
                self.queue.create_queue()
            except ResourceExistsError:
                pass

    def receive_message(self, timeout: int) -> str:
        message = self.queue.receive_message(visibility_timeout=timeout, timeout=timeout)
        if message is None:
            return None, None
        body = base64.b64decode(message.content).decode()
        return body, message

    def delete_message(self, message):
        self.queue.delete_message(message.id, message.pop_receipt)

    def enqueue(self, request_id):
        if type(request_id) is str:
            self.queue.send_message(base64.b64encode(request_id.encode()).decode())
        elif type(request_id) is list:
            for i in request_id:
                self.queue.send_message(base64.b64encode(i.encode()).decode())
    
    def get_poison_messages(self, delete = True):
        for message in self.poison_queue.receive_messages():
            decoded_message = base64.decodestring(message.content.encode()).decode()
            yield decoded_message
            if delete:
                self.poison_queue.delete_message(message)


class WorkerConnector:
    def __init__(self, worker_name: str, connection_string=None):
        if connection_string is None:
            self.connection_string = os.environ['AzureWebJobsStorage']
        else:
            self.connection_string = connection_string
        self.worker_name = worker_name
        self.metadata_repository = MetadataRepository(self.connection_string, worker_name + "Data", False)
        self.message_queue_client = MessageQueueClient(worker_name.lower(), worker_name.lower() + "-poison", self.connection_string, False)
    
    def exists(self) -> bool:
        return self.metadata_repository.exists()

    def trigger(self, data: List[str], params) -> str:
        request_id = self.metadata_repository.insert_raw_metadata(data, params)
        self.message_queue_client.enqueue(request_id)
        return request_id

    def trigger_blob(self, blob_name: str, params=None) -> str:
        request_id = self.metadata_repository.insert_blob_metadata(blob_name, params)
        self.message_queue_client.enqueue(request_id)
        return request_id
    
    def trigger_blobs(self, blob_names: List[str], params=None, guid=None) -> List[str]:
        if guid is None:
            guid = IdGenerator.generate_id()
        request_ids = self.metadata_repository.insert_blobs_metadata(blob_names, params, guid)
        self.message_queue_client.enqueue(request_ids)
        return request_ids
        
    def get_result(self, request_id: str) -> TaskResult:
        entity = self.metadata_repository.get_result_entity(request_id)
        entity.result = self._expand_result(entity.result)
        return entity

    def get_results(self, guid: str) -> List[TaskResult]:
        entities = self.metadata_repository.get_result_entities(guid)
        for entity in entities:
            entity.result = self._expand_result(entity.result)
        return entities

    def _expand_result(self, result):
        if result is None:
            return None

        # blob path: "{worker}/Requests/{pk}/{rk}"
        if len(result.split("/")) == 4:
            return self.reader.read_output_blob(result)
        return result


class Worker:
    def __init__(self, worker_name: str, 
        segment_limit=200, 
        connection_string=None, 
        return_only_source=True
    ):
        if connection_string is None:
            self.connection_string = os.environ['AzureWebJobsStorage']
        else:
            self.connection_string = connection_string
        self.worker_name = worker_name
        if segment_limit is not None:
            segment_limit = int(segment_limit)
        self.segment_limit = segment_limit
        self.reader = BlobReader(self.connection_string, return_only_source)
        self.metadata_repository = MetadataRepository(self.connection_string, worker_name + "Data", True)
        self.message_queue_client = MessageQueueClient(worker_name.lower(), worker_name.lower() + "-poison", self.connection_string, True)

    def process_messages_from_queue(self, process_func, timeout=3600, sleep_timeout=1):
        while True:
            time.sleep(sleep_timeout)
            message = self.message_queue_client.receive_message(timeout)
            if message is None:
                continue
            body, message = base64.b64decode(message.content).decode()
            self.process_message(body, process_func)
            self.message_queue_client.delete_message(message)

    def process_message(self, request_id: str, func):    
        metadata = self.metadata_repository.get_task_metadata(request_id)
        try:
            if metadata.blob_name is not None:
                self._process_blob(request_id, metadata, func)
            elif metadata.request is not None:
                self._process_raw_request(metadata, func)
        except Exception as e:
            self.metadata_repository.record_request_failure(metadata, e)
            self.metadata_repository.record_failure(request_id, e, self.worker_name)

    def process_poison_messages(self):
        try:
            for request_id in self.message_queue_client.get_poison_messages():
                pk, rk = IdGenerator.decode_id(request_id)
                self.metadata_repository.set_task_error(pk, rk, unhandled_exception_message, "")
                self.metadata_repository.insert_failure_record(self.worker_name, request_id, unhandled_exception_message, "")
        except ResourceNotFoundError:
            pass

    def _process_raw_request(self, metadata: TaskMetadata, func):
        request_body = json.loads(metadata.request)
        response = func(request_body["Data"], request_body["Params"])
        blob_name = f"{self.worker_name}/Request/{metadata.pk}/{metadata.rk}"
        metadata.result = blob_name
        self.reader.upload_output_blob(blob_name, json.dumps(response))
        self.metadata_repository.update_metadata(metadata)

    def _process_blob(self, request_id: str, metadata: TaskMetadata, func):
        try:
            if metadata.next_batch:
                result, failures = self._process_next_batch(metadata, func)
            else:
                result, failures = self._process_first_batch(metadata, func)
        except Exception as e:
            self._handle_exception_during_precessing(e, metadata, request_id)
            return

        if failures:
            self.metadata_repository.record_segment_failures(request_id, self.worker_name, failures)
        if metadata.next_batch is not None:
            self._move_task_to_next_stage(metadata, result, request_id)
        else:
            self._finalize_task(metadata, result)

    def _handle_exception_during_precessing(self, e, metadata: TaskMetadata, request_id: str):
        if metadata.retry_count == 3:
            raise e
        else:
            metadata.retry_count += 1
            self.metadata_repository.update_metadata(metadata)
            self.message_queue_client.enqueue(request_id)

    def _move_task_to_next_stage(self, metadata: TaskMetadata, result: list, request_id: str):
        output_blob = "%s/%s_%d" % (self.worker_name, metadata.blob_name, metadata.batch_count)
        serialized_result = "\n".join(json.dumps(r) for r in result)
        self.reader.upload_output_blob(output_blob, serialized_result)

        metadata.offset += len(result)
        metadata.batch_count += 1
        
        self.metadata_repository.update_metadata(metadata)
        self.message_queue_client.enqueue(request_id)

    def _finalize_task(self, metadata: TaskMetadata, result: list):
        serialized_result = "\n".join(json.dumps(r) for r in result)
        blob_name = "%s/%s" % (self.worker_name, metadata.blob_name)   
        if metadata.offset == 0:
            self.reader.upload_output_blob(blob_name, serialized_result)
        else:     
            content = []
            for batch in range(metadata.batch_count):
                blob_content = self.reader.read_output_blob("%s_%d" % (blob_name, batch))
                content.append(blob_content)
            content.append(serialized_result)
            self.reader.upload_output_blob(blob_name, "\n".join(content))
        metadata.state = "Completed"
        metadata.offset += len(result)
        metadata.next_batch = None
        self.metadata_repository.update_metadata(metadata)

    def _process_first_batch(self, metadata: TaskMetadata, func):
        batch, result, failures = [], [], []
        segments_iterator = self.reader.read_blob_by_segments(metadata.blob_name)
        for segment in segments_iterator:
            batch.append(segment)
            if self.segment_limit is not None and len(batch) == self.segment_limit:
                break

        if len(batch) > 0: 
            result, failures = func(batch, metadata.params)

        if self.segment_limit is None:
            # If there is no segment limit, then blob is processed in one batch
            return result, failures, []
            
        batch = []
        batch_id = 0
        for segment in segments_iterator:
            batch.append(segment)
            if len(batch) == self.segment_limit:
                batch_blob_name = self._get_batch_blob_name(metadata, batch_id)
                self.reader.upload_input_blob(batch_blob_name, json.dumps(batch, ensure_ascii=False))
                batch_id += 1
                batch = []

        if len(batch) > 0:
            batch_blob_name = self._get_batch_blob_name(metadata, batch_id)
            self.reader.upload_input_blob(batch_blob_name, json.dumps(batch, ensure_ascii=False))
            batch_id += 1

        if batch_id > 0:
            metadata.next_batch = self._get_batch_blob_name(metadata, 0)
            metadata.total_batches = batch_id

        return result, failures

    def _process_next_batch(self, metadata: TaskMetadata, func):
        segments_to_process = self.reader.read_input_blob(metadata.next_batch)
        result, failures = func(json.loads(segments_to_process), metadata.params)
        
        # Set correct segment indeces, based on offset
        for i in range(len(failures)):
            s, e, reason = failures[i]
            failures[i] = (s + metadata.offset, e + metadata.offset, reason)

        if metadata.batch_count != metadata.total_batches:
            metadata.next_batch = self._get_batch_blob_name(metadata, metadata.batch_count)
        else:
            metadata.next_batch = None
        return result, failures

    def _get_batch_blob_name(self, metadata: TaskMetadata, batch_id: int) -> str:
        blob_folder = metadata.blob_name.split('/')[0]
        return f"{blob_folder}/{metadata.rk}_{self.segment_limit}/{batch_id}"
