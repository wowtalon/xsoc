import logging
import os
from xplugin.plugin import Plugin
from flask import Flask, url_for
from jinja2 import Template

logger = logging.getLogger(__name__)

def log_func(message: str, level: str = "info"):
    logger.log(logging._nameToLevel.get(level.upper(), 1), f"PluginManager [{level}]: {message}")

logger.debug("Web Plugin module loaded.")

class WebPlugin(Plugin):

    def __init__(self):
        self.name = "WebPlugin"
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.separate_process = True
        self.continuous_run = True  # This plugin runs continuously
        self.app = None
        super().__init__()
        log_func("Web Plugin initialized.", level="debug")

    def get_template(self, template_name: str,) -> Template:
        template_file = os.path.join(self.template_path, template_name)
        with open(template_file, 'r') as file:
            template_content = file.read()
        return Template(template_content)

    def run_plugin(self, port=8080):
        log_func("Web Plugin is running.", level="info")
        log_func(f"Web Plugin will serve on port {port}", level="info")
        
        # Check if shutdown was requested before starting
        if self.is_shutdown_requested():
            log_func("Shutdown requested, not starting web server", level="info")
            return "Web Plugin shutdown requested"
            
        try:
            self.serve(port)
        except Exception as e:
            if not self.is_shutdown_requested():
                log_func(f"Error in web plugin: {e}", level="error")
            else:
                log_func("Web plugin stopped due to shutdown request", level="info")
        
        return "Web Plugin stopped"

    def serve_page(self, page: str) -> str:
        return f"Serving page: {page}"

    def serve(self, port=8080):
        try:
            from flask import Flask
        except ImportError:
            log_func("Flask not installed. Install with: pip install flask", level="error")
            return
            
        self.app = Flask(__name__)

        @self.app.route('/')
        def home():
            # Redirect to default xsoc home endpoint
            return xsoc_home('home')
        
        @self.app.route('/xsoc/<endpoint>')
        def xsoc_home(endpoint):
            try:
                xsoc_base_template = self.get_template("xsoc-base.html")
            except FileNotFoundError:
                # Fallback if base template doesn't exist
                xsoc_base_template = None
            template = self.get_template("xsoc-home.html")
            return template.render(endpoint=endpoint, xsoc_base_template=xsoc_base_template)

        @self.app.route('/overview')
        def overview():
            try:
                xsoc_base_template = self.get_template("xsoc-base.html")
            except FileNotFoundError:
                xsoc_base_template = None
            try:
                template = self.get_template("xsoc-overview.html")
            except FileNotFoundError:
                # Fallback to home template
                template = self.get_template("xsoc-home.html")
            return template.render(xsoc_base_template=xsoc_base_template)
        
        @self.app.route('/xsoc')
        def soc():
            try:
                xsoc_base_template = self.get_template("xsoc-base.html")
            except FileNotFoundError:
                xsoc_base_template = None
            try:
                template = self.get_template("xsoc-soc.html")
            except FileNotFoundError:
                template = self.get_template("xsoc-home.html")
            return template.render(xsoc_base_template=xsoc_base_template)
        
        @self.app.route('/xplugin')
        def xplugin():
            plugin_list = []
            if hasattr(self, 'xsoc_core'):
                plugin_list = self.xsoc_core.get("plugins", {}).get("built-in", []) + \
                              self.xsoc_core.get("plugins", {}).get("custom", [])
            try:
                xsoc_base_template = self.get_template("xsoc-base.html")
            except FileNotFoundError:
                xsoc_base_template = None
            try:
                template = self.get_template("xsoc-xplugin.html")
            except FileNotFoundError:
                template = self.get_template("xsoc-home.html")
            return template.render(xsoc_base_template=xsoc_base_template, plugin_list=plugin_list)

        @self.app.route('/settings')
        def settings():
            try:
                xsoc_base_template = self.get_template("xsoc-base.html")
            except FileNotFoundError:
                xsoc_base_template = None
            try:
                template = self.get_template("xsoc-settings.html")
            except FileNotFoundError:
                template = self.get_template("xsoc-home.html")
            return template.render(xsoc_base_template=xsoc_base_template)

        @self.app.route('/page/<page_name>')
        def serve_page_route(page_name):
            return self.serve_page(page_name)

        log_func(f"Starting web server on port {port}", level="info")
        
        # Run the Flask app with graceful shutdown support
        try:
            self.app.run(port=port, host='0.0.0.0', debug=False, use_reloader=False, threaded=True)
        except OSError as e:
            if "Address already in use" in str(e):
                log_func(f"Port {port} is already in use. Web server not started.", level="error")
            else:
                raise

