import json


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class TaskMetadata():
    def __init__(self, pk, rk, blob_name, params, offset, retry_count, batch_count, next_batch, request, result, error, trace, state, total_batches):
        self.pk = pk
        self.rk = rk
        self.blob_name = blob_name
        self.params = params
        self.offset = offset
        self.retry_count = retry_count
        self.batch_count = batch_count
        self.next_batch = next_batch
        self.request = request
        self.result = result
        self.error = error
        self.trace = trace
        self.state = state
        self.total_batches = total_batches

    def get_base_entity(self):
        return { "PartitionKey": self.pk, "RowKey": self.rk }

    def to_dict(self):
        row = {
            "PartitionKey": self.pk,
            "RowKey": self.rk,
            "BlobName": self.blob_name,
            "Request": self.request,
            "Result": self.result,
            "State": self.state,
            "Error": self.error,
            "StackTrace": self.trace,
            "RetryCount": self.retry_count,
            "Batch": self.batch_count,
            "Offset": self.offset,
            "TotalBatches": self.total_batches,
            "NextBatch": self.next_batch
        }
        if self.params is not None:
            row['Params'] = json.dumps(self.params, ensure_ascii=False)
        return row

    @staticmethod
    def create_from_dict(row):
        params, offset, retry_count, batch_count, next_batch, request, blob_name = None, 0, 0, 0, None, None, None
        total_batches = 0
        result, error, trace, state = None, None, None, None
        if 'BlobName' in row:
            blob_name = row['BlobName']
        if 'Params' in row:
            params = json.loads(row['Params'])
        if 'Offset' in row:
            offset = row['Offset']
        if 'RetryCount' in row:
            retry_count = row['RetryCount']
        if 'Batch' in row:
            batch_count = row['Batch']
        if 'NextBatch' in row:
            next_batch = row['NextBatch']
        if 'Request' in row:
            request = row['Request']
        if 'Result' in row:
            result = row['Result']
        if 'Error' in row:
            error = row['Error']
        if 'StackTrace' in row:
            trace = row['StackTrace']
        if "State" in row:
            state = row["State"]
        if "TotalBatches" in row:
            total_batches = row["TotalBatches"]
        return TaskMetadata(
            row['PartitionKey'], row['RowKey'],
            blob_name, params, offset, retry_count, batch_count, next_batch, request, result, error, trace, state, total_batches)


class TaskResult:
    def __init__(self, result, error_message, stack_trace, offset, request_id, state):
        self.result = result
        self.error_message = error_message
        self.stack_trace = stack_trace
        self.offset = offset
        self.request_id = request_id
        self.state = state

    @staticmethod
    def create_from_request_entity(entity):
        result, error, trace, offset, state = None, None, None, None, None
        if 'Result' in entity:
            result = entity['Result']
        if 'Error' in entity:
            error = entity['Error']
        if 'StackTrace' in entity:
            trace = entity['StackTrace']
        if 'Offset' in entity:
            offset = entity['Offset']
        if "State" in entity:
            state = entity["State"]

        request_id = "%s_%s" % (entity['PartitionKey'], entity['RowKey'])
        
        return TaskResult(result, error, trace, offset, request_id, state)

    def to_json(self):
        json_response = {"Completed": False, "RequestId": self.request_id}
        if self.result:
            json_response['Result'] = json.loads(self.result)
            json_response['Completed'] = True
        if self.error_message:
            json_response['Error'] = self.error_message
            json_response['StackTrace'] = self.stack_trace
            json_response['Completed'] = True
        if self.offset:
            json_response['Progress'] = self.offset
        if self.state and self.state == "Completed":
            json_response["Completed"] = True
        return json_response


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
