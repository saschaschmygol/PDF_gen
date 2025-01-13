import json

table_header = [['Рекоммендуемый срок', 'Инфекционное заболевание', 'Основание', '', ''],
              ['', '',
               'Региональный календарь профилактических прививок по Свердловской области (утвержден Приказом МЗ СО от 17 сентября 2024г. N 1881 - п)',
               'Национальный календарь профилактических прививок (утвержден Приказом МЗ РФ от 17 сентября 2024 г. N 2208-н)',
               'Календарь профилактических прививок по эпидемическим показаниям (утвержден Приказом МЗ РФ от 6 декабря 2021 г. N 1122-н)']]

text_top = ["<para alignment='center' fontName=TimesBold leading=20>Уведомление о необходимости прохождения иммунизации </para>", f"<para alignment='center' fontName=TimesBold>Уважаем",
            f'Уведомляем вас, что в 2025 году ВЫ подлежите иммунизации против : ',
            'Предлагаем вам пройти иммунизацию согласно графику, прописанному в уведомлении, в срок не позднее <font name=TimesBold>1 месяца</font> с начала периода, предложенного в графике'
            ' по профилактике конкретного заболевания, и предоставить данные старшей медсестре отделения(сотрудникам немедицинских и медицинских подразделений - '
            'в эпидемиологический отдел), для дальнейшего планирования последующих этапов иммунизации',
            'В случае <font name=TimesBold>отказа от прохождения иммунизации</font> Работодатель оставляет за собой право отстранять своего сотрудника от работы в рамках действующего законодательства'
            ' 1 месяца <font name=TimesBold>без сохранения заработной платы</font>']

text_bot = ['Дата <<_____>>___________2024г.',
            'Подпись направляемого на иммунизацию (с расшифровкой)_____________/___________',
            'Подпись сотрудника эпидемиологического отдела ___________/____________']

text_bot2 = ['Дополнительную информацию, что в соответствии с <u>Приложением №2 Приказом МЗ СО от 17 сентября 2024 г. № 2208-п:</u>',
             'П.8  Допускается введение вакцин (за исключением вакцин для профилактики туберкулеза),'
             'применяемых в рамках национального календаря профилактических прививок, календаря'
             'профилактических прививок по эпидемическим показаниям, регионального календаря профилактических'
             'прививок Свердловской области, регионального календаря профилактических прививок Свердловской'
             'области по эпидемическим показаниям в один календарный день разными шприцами в разные участки тела'
             '(одномоментно)… Для вакцин, имеющих один и тот же антигенный состав, интервал в рамках первичного'
             'комплекса прививок должен составлять минимум 1 месяц. Вместе с тем, в настоящее время в соответствии с'
             'международной практикой, допускается введение неживых вакцин с любым интервалом между собой, при'
             'введении живых вакцин рекомендуется интервал 1 месяц, между живой и неживой вакцинами, также'
             'допустим любой интервал.',
             'П.11 Иммунизация в рамках регионального календаря вакцинами, не входящими в национальный'
             'календарь профилактических прививок и календарь профилактических прививок по эпидемическим'
             'показаниям, проводится за счет средств муниципальных образований, средств граждан и других'
             'источников, не запрещенных законодательством.']



keys_list = ['table_header', 'text_top', 'text_bot', 'text_bot2']
values_list = [table_header, text_top, text_bot, text_bot2]

with open('data_dict.json', 'r', encoding='utf-8') as f:
    loaded_dict = json.load(f)  # словарь
    for i in range(len(keys_list)):
        loaded_dict[keys_list[i]] = values_list[i]

with open('data_dict.json', 'w', encoding='utf-8') as f:
    json.dump(loaded_dict, f, ensure_ascii=False, indent=4)
