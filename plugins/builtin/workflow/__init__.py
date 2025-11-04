import os
from xplugin.plugin import Plugin
from xplugin.logger import xlogger
import jinja2

xlogger.debug("Workflow Plugin initialized.")

def parse_workflow_config(config_path: str):
    """Parse a workflow from a YAML configuration file."""
    import yaml
    with open(config_path, 'r') as file:
        workflow = yaml.safe_load(file)
    xlogger.debug(f"Parsed workflow from {config_path}: {workflow}")
    return workflow


class WorkflowPlugin(Plugin):

    _workflow = None  # Placeholder for workflow object
    separate_process = True
    singleton = False

    def __init__(self, built_in: bool = False):
        super().__init__()
        self.description = "A plugin to manage workflows"
        self.built_in = built_in
        __import__(f"{__name__}.tools")


    def load_config(self, config):
        for workflow_config_path in os.listdir(config.get('workflow_path', '')):
            xlogger.debug(f"Loading workflow config: {workflow_config_path}")
            yield self, {"workflow_config_path": os.path.join(config.get('workflow_path', ''), workflow_config_path)}
        

    def run(self, workflow_config_path: str = None):
        # self.workflow_config_path = workflow_config_path
        xlogger.debug(f"Workflow Plugin initialized with config path: {workflow_config_path}")
        workflow = self.create_workflow(workflow_config_path) if workflow_config_path else None
        xlogger.debug("Running Workflow Plugin")
        if workflow:
            xlogger.debug(f"Running workflow: {workflow['name']}")
            return self.run_workflow(workflow)
        return "Workflow Plugin is running"
    

    def create_workflow(self, config_path: str):
        """Create a workflow from a configuration file."""
        workflow = parse_workflow_config(config_path)
        xlogger.debug(f"Workflow created from {config_path}: {workflow}")
        return workflow
    
    def run_workflow(self, workflow):
        """Run a workflow."""
        xlogger.debug(f"Running workflow: {workflow}")
        context = {
            "env": workflow.get('env', {}),
            "steps": {}
        }
        for step in workflow.get('steps', []):
            xlogger.debug(f"Executing step: {step}")
            # Here you would add logic to execute each step
            parameters = step.get('parameters', {})
            xlogger.debug(f"Original parameters: {parameters}")
            if isinstance(parameters, dict):
                for key, value in parameters.items():
                    parameters[key] = jinja2.Template(str(value)).render(context)
            xlogger.debug(f"Resolved parameters: {parameters}")
            match step.get('action'):
                case 'tool':
                    tool_name = step.get('target')
                    xlogger.debug(f"Running tool {tool_name} with parameters {parameters}")
                    # Placeholder for actual tool execution
                    # Dynamic call 
                    result = globals()['tools'].__dict__[tool_name](parameters)
                    xlogger.debug(f"Tool {tool_name} result: {result}")
                case 'wait':
                    duration = step.get('duration', 1)
                    # xlogger.debug(f"Waiting for {duration} seconds")
                    self.wait_or_shutdown(timeout=duration)
                case 'plugin':
                    plugin_name, tool_name = step.get('target').split('.')
                    # Dynamic call
                    if self.plugin_manager and self.plugin_manager.get_plugin(plugin_name):
                        plugin_instance = self.plugin_manager.get_plugin(plugin_name)
                    else:
                        xlogger.error(f"Plugin {plugin_name} not found")
                        raise ValueError(f"Plugin {plugin_name} not found")
                    result = getattr(plugin_instance, tool_name)(**parameters)
                    # xlogger.debug(f"Plugin {plugin_name} result: {result}")
            context['steps'][step['name']] = result
            xlogger.debug(context)
        # Placeholder for actual workflow execution logic
        return f"Workflow {workflow['name']} executed successfully"
