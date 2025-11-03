from xplugin.plugin import Plugin
from xplugin.logger import xlogger
import jinja2

xlogger.info("Workflow Plugin initialized.")

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

    def __init__(self):
        super().__init__()
        self.description = "A plugin to manage workflows"
        __import__(f"{__name__}.tools")
        

    def run_plugin(self, workflow_config_path: str = None):
        self.workflow_config_path = workflow_config_path
        xlogger.debug(f"Workflow Plugin initialized with config path: {workflow_config_path}")
        self._workflow = self.create_workflow(workflow_config_path) if workflow_config_path else None
        xlogger.debug("Running Workflow Plugin")
        if self._workflow:
            xlogger.debug(f"Running workflow: {self._workflow['name']}")
            return self.run_workflow(self._workflow)
        return "Workflow Plugin is running"
    

    def create_workflow(self, config_path: str):
        """Create a workflow from a configuration file."""
        workflow = parse_workflow_config(config_path)
        print(f"Workflow created from {config_path}: {workflow}")
        return workflow
    
    def run_workflow(self, workflow):
        """Run a workflow."""
        print(f"Running workflow: {workflow}")
        context = {
            "env": workflow.get('env', {}),
            "steps": {}
        }
        for step in workflow.get('steps', []):
            print(f"Executing step: {step}")
            # Here you would add logic to execute each step
            parameters = step.get('parameters', {})
            xlogger.debug(f"Original parameters: {parameters}")
            for key, value in parameters.items():
                parameters[key] = jinja2.Template(str(value)).render(context)
                # if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                #     ref_keys = value[1:-1].split('.')
                    
                #     if ref_keys[0] == 'env':
                #         ref_context = context['env']
                #         ref_keys = ref_keys[1:]
                #     else:
                #         ref_context = context['steps']
                #     for ref_key in ref_keys:
                #         if ref_key in ref_context:
                #             ref_context = ref_context[ref_key]
                #         else:
                #             raise ValueError(f"Reference {value} not found in context")
                #     parameters[key] = ref_context
            xlogger.debug(f"Resolved parameters: {parameters}")
            match step.get('action'):
                case 'tool':
                    tool_name = step.get('target')
                    parameters = step.get('parameters', {})
                    # xlogger.debug(f"Running tool {tool_name} with parameters {parameters}")
                    # Placeholder for actual tool execution
                    # Dynamic call 
                    result = globals()['tools'].__dict__[tool_name](**parameters)
                    xlogger.debug(f"Tool {tool_name} result: {result}")
                case 'wait':
                    duration = step.get('duration', 1)
                    # xlogger.debug(f"Waiting for {duration} seconds")
                    self.wait_or_shutdown(timeout=duration)
                case 'plugin':
                    plugin_name, tool_name = step.get('target').split('.')
                    parameters = step.get('parameters', {})
                    # xlogger.debug(f"Invoking plugin {plugin_name} with parameters {parameters}")
                    # xlogger.debug(self.xsoc_core['plugins'])
                    # Placeholder for actual plugin invocation
                    # Dynamic call
                    if plugin_name in self.xsoc_core['plugins']['built-in']:
                        plugin_instance = self.xsoc_core['plugins']['built-in'][plugin_name]
                    elif plugin_name in self.xsoc_core['plugins']['custom']:
                        plugin_instance = self.xsoc_core['plugins']['custom'][plugin_name]
                    else:
                        xlogger.error(f"Plugin {plugin_name} not found")
                        raise ValueError(f"Plugin {plugin_name} not found")
                    result = getattr(plugin_instance, tool_name)(**parameters)
                    # xlogger.debug(f"Plugin {plugin_name} result: {result}")
            context['steps'][step['name']] = result
            xlogger.debug(context)
        # Placeholder for actual workflow execution logic
        return f"Workflow {workflow['name']} executed successfully"
