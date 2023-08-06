# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-11-20 16:16:22
:LastEditTime: 2021-12-16 15:52:38
:LastEditors: HuangJingCan
:description: appinfo相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.base.base_info_model import *


class GetAppExpireHandler(SevenBaseHandler):
    """
    :description: 获取小程序是否过期未续费
    """
    def get_async(self):
        """
        :description: 获取小程序是否过期未续费
        :return info
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        now_date = self.get_now_datetime()

        app_info = AppInfoModel(context=self).get_entity("app_id=%s", params=[app_id])
        if not app_info:
            return self.reponse_json_error("NoAct", "对不起，找不到该小程序")

        info = {}
        if app_info.expiration_date == "1900-01-01 00:00:00":
            info["is_expire"] = 0
        elif TimeHelper.format_time_to_datetime(now_date) > TimeHelper.format_time_to_datetime(app_info.expiration_date):
            info["is_expire"] = 1
        else:
            info["is_expire"] = 0

        base_info = BaseInfoModel(context=self).get_entity()
        if base_info:
            info["client_ver"] = base_info.client_ver

        return self.reponse_json_success(info)