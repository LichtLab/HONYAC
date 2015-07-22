# -*- coding: utf-8 -*-
from microsofttranslator import Translator
translator = Translator('shosekine', '2GFvzrRkechE3izlMfvRHRs+0y9VEcwpMUvVJhkPVOM=')
print translator.translate(u"明日天気だったら散歩に行く予定だよ", "en")