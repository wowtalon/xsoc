from xplugin.plugin import Plugin
from xplugin.logger import xlogger
from apscheduler.schedulers.background import BackgroundScheduler
import plugins.builtin.workflow.tools  as tools
import os


class CronPlugin(Plugin):

    separate_process = True
    singleton = False
    started = False

    def __init__(self, built_in: bool = False):
        super().__init__(built_in)
        self.description = "A plugin to manage cron jobs"
        self.scheduler = BackgroundScheduler()
        self.continuous_run = True


    def parse_cron_config(self, config_path: str):
        """Parse a cron job from a YAML configuration file."""
        import yaml
        with open(config_path, 'r') as file:
            cron_config = yaml.safe_load(file)
        xlogger.debug(f"Parsed cron config from {config_path}: {cron_config}")
        return cron_config


    def load_config(self, config):
        cron_path = config.get("cron_path", {})
        for cron_file in os.listdir(cron_path):
            xlogger.debug(f"Loading cron config: {cron_file}")
            # Load job yaml
            job_config = self.parse_cron_config(os.path.join(cron_path, cron_file))
            cron_job = self.create_cron_job(job_config)
            if cron_job:
                yield self, cron_job
            else:
                yield None, None

    
    def shutdown(self):
        xlogger.debug("Shutting down Cron Plugin scheduler...")
        self.scheduler.shutdown(wait=True)
        return super().shutdown()
    

    def run(self, **kwargs):
        if not self.started:
            xlogger.debug("Starting Cron Plugin scheduler...")
            self.scheduler.start()
            self.started = True
            xlogger.debug("Cron Plugin scheduler started.")
        try:
            while not self.shutdown_event.is_set():
                pass
        except KeyboardInterrupt:
            xlogger.debug("KeyboardInterrupt received in Cron Plugin, shutting down...")
            self.shutdown()
    
    def create_cron_job(self, job_config):
        xlogger.debug(f"Creating cron job with config: {job_config}")
        # Logic to create a cron job
        try:
            if not job_config.get('enabled', True):
                xlogger.debug("Cron job is disabled, skipping creation.")
                return None
            # xlogger.debug(f"Creating cron job: {job_config['job']['params']}")
            if job_config['job']['type'] == 'tool':
                self.scheduler.add_job(func=getattr(tools, job_config['job']['target']), trigger='cron', **job_config['schedule'], args=[], kwargs=job_config['job'].get('params', {}))
            elif job_config['job']['type'] == 'function':
                self.scheduler.add_job(func=globals()[job_config['job']['target']], trigger='cron', **job_config['schedule'], args=[], kwargs=job_config['job'].get('params', {}))
            elif job_config['job']['type'] == 'workflow':
                xlogger.debug("Creating cron job for workflow")
                workflow_plugin = self.plugin_manager.get_plugin('workflow')
                xlogger.debug(f"Retrieved workflow plugin: {workflow_plugin}")
                xlogger.debug(workflow_plugin.get_workflow(job_config['job']['target']))
                if workflow_plugin and workflow_plugin.get_workflow(job_config['job']['target']):
                    workflow = workflow_plugin.get_workflow(job_config['job']['target'])
                    xlogger.debug(f"Scheduling workflow: {workflow}")
                    if workflow:
                        self.scheduler.add_job(func=workflow_plugin.run_workflow, trigger='cron', **job_config['schedule'], args=[workflow], kwargs=job_config['job'].get('params', {}))
            else:
                xlogger.error(f"Unknown job type: {job_config['job']['type']}")
                raise ValueError(f"Unknown job type: {job_config['job']['type']}")
            xlogger.debug(f"Cron job created with config: {job_config}")
            return job_config
        except Exception as e:
            xlogger.error(f"Error creating cron job: {e}")
        return f"Cron job created with config: {job_config}"
