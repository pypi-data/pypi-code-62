#      Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _


class Holiday(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    date = models.DateField(_("Date"))

    class Meta:
        ordering = ['date']
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")

    def __str__(self):  # __unicode__ on Python 2
        # Returns the person's full name.
        return "{} - {}".format(self.name, self.date)
