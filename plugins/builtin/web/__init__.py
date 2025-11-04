from xplugin.plugin import Plugin
from flask import Flask, url_for
from jinja2 import Template
from xplugin.logger import xlogger
import logging
import os

xlogger.debug("Web Plugin module loaded.")

class WebPlugin(Plugin):

    def __init__(self, built_in: bool = False):
        self.name = "WebPlugin"
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.separate_process = True
        self.continuous_run = True  # This plugin runs continuously
        self.app = None
        self.is_built_in = built_in
        super().__init__()
        xlogger.debug("Web Plugin initialized.")

    def get_template(self, template_name: str,) -> Template:
        template_file = os.path.join(self.template_path, template_name)
        with open(template_file, 'r') as file:
            template_content = file.read()
        return Template(template_content)


    def run(self, host="0.0.0.0", port=8080):
        xlogger.debug("Web Plugin is running.")
        xlogger.debug(f"Web Plugin will serve on port {port}")
        
        # Check if shutdown was requested before starting
        if self.is_shutdown_requested():
            xlogger.debug("Shutdown requested, not starting web server")
            return "Web Plugin shutdown requested"
            
        try:
            self.serve(host, port)
        except Exception as e:
            if not self.is_shutdown_requested():
                xlogger.error(f"Error in web plugin: {e}")
            else:
                xlogger.debug("Web plugin stopped due to shutdown request")
        
        return "Web Plugin stopped"

    def serve_page(self, page: str) -> str:
        return f"Serving page: {page}"

    def serve(self, host="0.0.0.0", port=8080):
        try:
            from flask import Flask
        except ImportError:
            xlogger.error("Flask not installed. Install with: pip install flask")
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

        xlogger.debug(f"Starting web server on port {port}")
        
        # Run the Flask app with graceful shutdown support
        try:
            self.app.run(port=port, host=host, debug=False, use_reloader=False, threaded=True)
        except OSError as e:
            if "Address already in use" in str(e):
                xlogger.error(f"Port {port} is already in use. Web server not started.")
            else:
                raise

