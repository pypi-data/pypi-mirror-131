from tgaflow.base import BaseTask
from tgautil.download_util import DownloadUtil
from tgautil.sql_format import SQLFormat


class DownloadTask(BaseTask):
    def __init__(self, flow_id, params):
        self.task_name = 'download'
        super().__init__(flow_id, params, ['check', 'refresh'])

    def process(self):
        sqlFormat = SQLFormat()
        du = DownloadUtil({
            'name': self.params['name'],
            'sql': sqlFormat.run(self.params)

        })
        filepath = du.run()
        if filepath is None:
            return False, {'result': filepath}
        else:
            return True, {'filepath': filepath}
