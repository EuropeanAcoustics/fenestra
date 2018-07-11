#! /usr/bin/env python
# -*- coding:utf8 -*-

from django import template
import fenestra.settings as settings


register = template.Library()


@register.tag
def app_version(parser, token):
    return AppVersionNode()


class AppVersionNode(template.Node):
    def render(self, context):
        return settings.APP_VERSION
