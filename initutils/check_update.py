import bpy
import os
from .. import addon_updater_ops
from datetime import datetime, timedelta


class CheckUpdate(bpy.types.Operator):
    """
    Check for an update according to the user preferences.

    This operator is meant to be called when the user adds a transform
    modifer with the addon. If time has elapsed past the user-established
    check interval, this will trigger an update check.

    If there is an update available, it will trigger the dialog popup,
    else the check interval is reset.
    """
    bl_idname = "vse_transform_tools.check_update"
    bl_label = "Check Update"
    bl_description = "Check for VSE Transform Tools Update"

    def update_check_responder(self, update_ready):
        if update_ready:
            addon_updater_ops.background_update_callback(update_ready)

        updater = addon_updater_ops.updater
        updater.json["last_check"] = str(datetime.now())
        updater.save_updater_json()

    def execute(self, context):
        folder = os.path.dirname(__file__)
        home = os.path.abspath(os.path.join(folder, '..'))
        addon_name = os.path.basename(home)
        settings = context.user_preferences.addons[addon_name].preferences

        if not settings.auto_check_update:
            return {'FINISHED'}

        updater = addon_updater_ops.updater
        check_update = False

        if "last_check" not in updater.json or updater.json["last_check"] == "":
            check_update = True

        else:
            months = settings.updater_intrval_months
            days = settings.updater_intrval_days
            hours = settings.updater_intrval_hours
            minutes = settings.updater_intrval_minutes

            interval = timedelta(
                days=(months * 30) + days, hours=hours, minutes=minutes)

            now = datetime.now()
            last_check = datetime.strptime(
                updater.json['last_check'], "%Y-%m-%d %H:%M:%S.%f")
            diff = now - last_check

            if diff > interval:
                check_update = True

        if check_update:
            if not updater.update_ready and not updater.async_checking:
                updater.start_async_check_update(False, self.update_check_responder)

        return {'FINISHED'}
