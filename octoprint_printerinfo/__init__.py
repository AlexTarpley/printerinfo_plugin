import octoprint.plugin
from octoprint.server import admin_permission
from octoprint.events import Events


class PrinterinfoPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.BlueprintPlugin,
    octoprint.plugin.EventHandlerPlugin
):

    def on_after_startup(self):
        profile = self._printer_profile_manager.get_default()
        self._logger.info("Printer profile name: {}".format(profile["name"]))

    def on_event(self, event, payload):
        if event == Events.FILE_ADDED:
            self._logger.info("New print job added!")
            job_id = payload.get("job", {}).get("id")
            if job_id is not None:
                job_data = self._printer.get_current_job()
                if job_data is not None:
                    self._logger.info("Job data: %s", job_data)
                    # Update your job object here
                else:
                    self._logger.warning(
                        "Failed to get job data for job id: %s", job_id)

   # class JobInfoPlugin(octoprint.plugin.EventHandlerPlugin):
   #
   #     def on_event(self, event, payload):
   #         if event == Events.PRINT_JOB_ADDED:
   #             self._logger.info("New print job added!")
   #             job_id = payload.get("job", {}).get("id")
   #             if job_id is not None:
   #                 job_data = self._printer.get_job_data(job_id)
   #                 if job_data is not None:
   #                     self._logger.info("Job data: %s", job_data)
   #                     # Update your job object here
   #                 else:
   #                     self._logger.warning("Failed to get job data for job id: %s", job_id)
   #

    # Define your plugin's asset files to automatically include in the
    # core UI here.
    def get_assets(self):
        return {
            #"js": ["js/printerinfo.js"],
            #"css": ["css/printerinfo.css"],
            #"less": ["less/printerinfo.less"]
        }

    # Define the API endpoint for getting the printer profile information
    @octoprint.plugin.BlueprintPlugin.route("/api/printer/profile", methods=["GET"])
    @octoprint.plugin.BlueprintPlugin.requires_access(admin_permission)
    #@octoprint.plugin.BlueprintPlugin.route("/api/job", methods=["GET"])
    #@octoprint.plugin.BlueprintPlugin.requires_access(status_permission)
    def get_printer_profile(self):
        profile = self._printer_profile_manager.get_default()
        #profile = octoprint.printer.profiles()
        return profile


__plugin_name__ = "Printerinfo Plugin"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrinterinfoPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
