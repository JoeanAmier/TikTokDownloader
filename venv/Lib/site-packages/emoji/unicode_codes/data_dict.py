"""Data containing all current emoji
Extracted from https://unicode.org/Public/emoji/latest/emoji-test.txt
and https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt
See utils/generate_emoji.py

+----------------+-------------+------------------+-------------------+
| Emoji Version  |    Date     | Unicode Version  | Data File Comment |
+----------------+-------------+------------------+-------------------+
| N/A            | 2010-10-11  | Unicode 6.0      | E0.6              |
| N/A            | 2014-06-16  | Unicode 7.0      | E0.7              |
| Emoji 1.0      | 2015-06-09  | Unicode 8.0      | E1.0              |
| Emoji 2.0      | 2015-11-12  | Unicode 8.0      | E2.0              |
| Emoji 3.0      | 2016-06-03  | Unicode 9.0      | E3.0              |
| Emoji 4.0      | 2016-11-22  | Unicode 9.0      | E4.0              |
| Emoji 5.0      | 2017-06-20  | Unicode 10.0     | E5.0              |
| Emoji 11.0     | 2018-05-21  | Unicode 11.0     | E11.0             |
| Emoji 12.0     | 2019-03-05  | Unicode 12.0     | E12.0             |
| Emoji 12.1     | 2019-10-21  | Unicode 12.1     | E12.1             |
| Emoji 13.0     | 2020-03-10  | Unicode 13.0     | E13.0             |
| Emoji 13.1     | 2020-09-15  | Unicode 13.0     | E13.1             |
| Emoji 14.0     | 2021-09-14  | Unicode 14.0     | E14.0             |
| Emoji 15.0     | 2022-09-13  | Unicode 15.0     | E15.0             |
| Emoji 15.1     | 2023-09-12  | Unicode 15.1     | E15.1             |
| Emoji 16.0     | 2024-09-10  | Unicode 16.0     | E16.0             |

               http://www.unicode.org/reports/tr51/#Versioning

"""

__all__ = ['STATUS', 'LANGUAGES']

from typing import Any, Dict, List


component = 1
fully_qualified = 2
minimally_qualified = 3
unqualified = 4

STATUS: Dict[str, int] = {
    'component': component,
    'fully_qualified': fully_qualified,
    'minimally_qualified': minimally_qualified,
    'unqualified': unqualified,
}

LANGUAGES: List[str] = [
    'en',
    'es',
    'ja',
    'ko',
    'pt',
    'it',
    'fr',
    'de',
    'fa',
    'id',
    'zh',
    'ru',
    'tr',
    'ar',
]


# The following is only an example of how the EMOJI_DATA dict is structured.
# The real data is loaded from the json files at runtime, see unicode_codes/__init__.py
EMOJI_DATA: Dict[str, Dict[str, Any]] = {
    '\U0001f947': {  # 🥇
        'en': ':1st_place_medal:',
        'status': fully_qualified,
        'E': 3,
        'de': ':goldmedaille:',
        'es': ':medalla_de_oro:',
        'fr': ':médaille_d’or:',
        'ja': ':金メダル:',
        'ko': ':금메달:',
        'pt': ':medalha_de_ouro:',
        'it': ':medaglia_d’oro:',
        'fa': ':مدال_طلا:',
        'id': ':medali_emas:',
        'zh': ':金牌:',
        'ru': ':золотая_медаль:',
        'tr': ':birincilik_madalyası:',
        'ar': ':ميدالية_مركز_أول:',
    },
    '\U0001f948': {  # 🥈
        'en': ':2nd_place_medal:',
        'status': fully_qualified,
        'E': 3,
        'de': ':silbermedaille:',
        'es': ':medalla_de_plata:',
        'fr': ':médaille_d’argent:',
        'ja': ':銀メダル:',
        'ko': ':은메달:',
        'pt': ':medalha_de_prata:',
        'it': ':medaglia_d’argento:',
        'fa': ':مدال_نقره:',
        'id': ':medali_perak:',
        'zh': ':银牌:',
        'ru': ':серебряная_медаль:',
        'tr': ':ikincilik_madalyası:',
        'ar': ':ميدالية_مركز_ثان:',
    },
    '\U0001f949': {  # 🥉
        'en': ':3rd_place_medal:',
        'status': fully_qualified,
        'E': 3,
        'de': ':bronzemedaille:',
        'es': ':medalla_de_bronce:',
        'fr': ':médaille_de_bronze:',
        'ja': ':銅メダル:',
        'ko': ':동메달:',
        'pt': ':medalha_de_bronze:',
        'it': ':medaglia_di_bronzo:',
        'fa': ':مدال_برنز:',
        'id': ':medali_perunggu:',
        'zh': ':铜牌:',
        'ru': ':бронзовая_медаль:',
        'tr': ':üçüncülük_madalyası:',
        'ar': ':ميدالية_مركز_ثالث:',
    },
    '\U0001f18e': {  # 🆎
        'en': ':AB_button_(blood_type):',
        'status': fully_qualified,
        'E': 0.6,
        'alias': [':ab:', ':ab_button_blood_type:'],
        'de': ':großbuchstaben_ab_in_rotem_quadrat:',
        'es': ':grupo_sanguíneo_ab:',
        'fr': ':groupe_sanguin_ab:',
        'ja': ':血液型ab型:',
        'ko': ':에이비형:',
        'pt': ':botão_ab_(tipo_sanguíneo):',
        'it': ':gruppo_sanguigno_ab:',
        'fa': ':دکمه_آ_ب_(گروه_خونی):',
        'id': ':tombol_ab_(golongan_darah):',
        'zh': ':AB型血:',
        'ru': ':IV_группа_крови:',
        'tr': ':ab_düğmesi_(kan_grubu):',
        'ar': ':زر_ab_(فئة_الدم):',
    },
    '\U0001f3e7': {  # 🏧
        'en': ':ATM_sign:',
        'status': fully_qualified,
        'E': 0.6,
        'alias': [':atm:', ':atm_sign:'],
        'de': ':symbol_geldautomat:',
        'es': ':señal_de_cajero_automático:',
        'fr': ':distributeur_de_billets:',
        'ja': ':atm:',
        'ko': ':에이티엠:',
        'pt': ':símbolo_de_caixa_automático:',
        'it': ':simbolo_dello_sportello_bancomat:',
        'fa': ':نشان_عابربانک:',
        'id': ':tanda_atm:',
        'zh': ':取款机:',
        'ru': ':значок_банкомата:',
        'tr': ':atm_işareti:',
        'ar': ':علامة_ماكينة_صرف_آلي:',
    },
    '\U0001f170\U0000fe0f': {  # 🅰️
        'en': ':A_button_(blood_type):',
        'status': fully_qualified,
        'E': 0.6,
        'alias': [':a:', ':a_button_blood_type:'],
        'variant': True,
        'de': ':großbuchstabe_a_in_rotem_quadrat:',
        'es': ':grupo_sanguíneo_a:',
        'fr': ':groupe_sanguin_a:',
        'ja': ':血液型a型:',
        'ko': ':에이형:',
        'pt': ':botão_a_(tipo_sanguíneo):',
        'it': ':gruppo_sanguigno_a:',
        'fa': ':دکمه_آ_(گروه_خونی):',
        'id': ':tombol_a_(golongan_darah):',
        'zh': ':A型血:',
        'ru': ':ii_группа_крови:',
        'tr': ':a_düğmesi_(kan_grubu):',
        'ar': ':زر_a:',
    },
    '\U0001f170': {  # 🅰
        'en': ':A_button_(blood_type):',
        'status': unqualified,
        'E': 0.6,
        'alias': [':a:', ':a_button_blood_type:'],
        'variant': True,
        'de': ':großbuchstabe_a_in_rotem_quadrat:',
        'es': ':grupo_sanguíneo_a:',
        'fr': ':groupe_sanguin_a:',
        'ja': ':血液型a型:',
        'ko': ':에이형:',
        'pt': ':botão_a_(tipo_sanguíneo):',
        'it': ':gruppo_sanguigno_a:',
        'fa': ':دکمه_آ_(گروه_خونی):',
        'id': ':tombol_a_(golongan_darah):',
        'zh': ':A型血:',
        'ru': ':II_группа_крови:',
        'tr': ':a_düğmesi_(kan_grubu):',
        'ar': ':زر_a:',
    },
    '\U0001f1e6\U0001f1eb': {  # 🇦🇫
        'en': ':Afghanistan:',
        'status': fully_qualified,
        'E': 2,
        'alias': [':flag_for_Afghanistan:', ':afghanistan:'],
        'de': ':flagge_afghanistan:',
        'es': ':bandera_afganistán:',
        'fr': ':drapeau_afghanistan:',
        'ja': ':旗_アフガニスタン:',
        'ko': ':깃발_아프가니스탄:',
        'pt': ':bandeira_afeganistão:',
        'it': ':bandiera_afghanistan:',
        'fa': ':پرچم_افغانستان:',
        'id': ':bendera_afganistan:',
        'zh': ':阿富汗:',
        'ru': ':флаг_Афганистан:',
        'tr': ':bayrak_afganistan:',
        'ar': ':علم_أفغانستان:',
    },
    '\U0001f1e6\U0001f1f1': {  # 🇦🇱
        'en': ':Albania:',
        'status': fully_qualified,
        'E': 2,
        'alias': [':flag_for_Albania:', ':albania:'],
        'de': ':flagge_albanien:',
        'es': ':bandera_albania:',
        'fr': ':drapeau_albanie:',
        'ja': ':旗_アルバニア:',
        'ko': ':깃발_알바니아:',
        'pt': ':bandeira_albânia:',
        'it': ':bandiera_albania:',
        'fa': ':پرچم_آلبانی:',
        'id': ':bendera_albania:',
        'zh': ':阿尔巴尼亚:',
        'ru': ':флаг_Албания:',
        'tr': ':bayrak_arnavutluk:',
        'ar': ':علم_ألبانيا:',
    },
    '\U0001f1e9\U0001f1ff': {  # 🇩🇿
        'en': ':Algeria:',
        'status': fully_qualified,
        'E': 2,
        'alias': [':flag_for_Algeria:', ':algeria:'],
        'de': ':flagge_algerien:',
        'es': ':bandera_argelia:',
        'fr': ':drapeau_algérie:',
        'ja': ':旗_アルジェリア:',
        'ko': ':깃발_알제리:',
        'pt': ':bandeira_argélia:',
        'it': ':bandiera_algeria:',
        'fa': ':پرچم_الجزایر:',
        'id': ':bendera_aljazair:',
        'zh': ':阿尔及利亚:',
        'ru': ':флаг_Алжир:',
        'tr': ':bayrak_cezayir:',
        'ar': ':علم_الجزائر:',
    },
    '\U0001f1e6\U0001f1f8': {  # 🇦🇸
        'en': ':American_Samoa:',
        'status': fully_qualified,
        'E': 2,
        'alias': [':flag_for_American_Samoa:', ':american_samoa:'],
        'de': ':flagge_amerikanisch-samoa:',
        'es': ':bandera_samoa_americana:',
        'fr': ':drapeau_samoa_américaines:',
        'ja': ':旗_米領サモア:',
        'ko': ':깃발_아메리칸_사모아:',
        'pt': ':bandeira_samoa_americana:',
        'it': ':bandiera_samoa_americane:',
        'fa': ':پرچم_ساموآی_امریکا:',
        'id': ':bendera_samoa_amerika:',
        'zh': ':美属萨摩亚:',
        'ru': ':флаг_Американское_Самоа:',
        'tr': ':bayrak_amerikan_samoası:',
        'ar': ':علم_ساموا_الأمريكية:',
    },
}
