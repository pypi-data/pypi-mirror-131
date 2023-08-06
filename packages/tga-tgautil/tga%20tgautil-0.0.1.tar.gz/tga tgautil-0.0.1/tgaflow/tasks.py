from tgaflow.check import CheckTask
from tgaflow.download import DownloadTask
from tgaflow.refresh import RefreshTask
from proj.celery import app


# params={'projectId': 4, 'clusterId': 168}
@app.task
def refresh(flow_id, params):
    refreshTask = RefreshTask(flow_id, params)
    refreshTask.handle()


# params={'projectId': 4, 'clusterId': 168}
@app.task
def check(flow_id, params):
    checkTask = CheckTask(flow_id, params)
    checkTask.handle()


# params={'name': 'test', 'sql': 'select * from'}
@app.task
def download(flow_id, params):
    downloadTask = DownloadTask(flow_id, params)
    downloadTask.handle()