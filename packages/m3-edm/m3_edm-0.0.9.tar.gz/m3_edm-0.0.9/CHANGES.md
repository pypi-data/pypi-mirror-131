0.0.9

* BOBUH-18883 Удаление модели-перечисления статус ЭЦП; 
* BOBUH-18883 Дополнение модели подписи электронного документа.

0.0.8

* Исправление опечатки в имени поля кеша.

0.0.7

* Добавлен url пакета;
* Дополнен MANIFEST.in.

0.0.6
* BOZIK-29158 Вынос общей логики по смене статуса документа.

0.0.5
* BOBUH-18943 Изменение типа даты с даты времени;
* BOBUH-18943 Изменение базовых классов моделей-перечислений; 
* BOBUH-18943 В BaseElectronicDocumentTransitionPermission добавлено поле abbreviation;
* BOBUH-18943 Рефакторинг Вида документа;
* BOBUH-18943 Дополнен .gitignore.

0.0.4

* BOBUH-18362 Замена базовой модели у BaseElectronicDocumentStatus и BaseElectronicSignatureStatus на CharModelEnum; 
* BOBUH-18362 Добавление базового класса модели-перечисления прав на функции BaseElectronicDocumentFunctionPermission;
* BOBUH-18362 Переименована модель BaseElectronicDocumentFunctionPermission в BaseElectronicDocumentTransitionPermission;
* BOBUH-18362 В модель BaseElectronicDocumentTransition добавлены поля title и permission;
* BOBUH-18362 Из модели BaseElectronicDocumentEditingLog убраны поля from_status и to_status, добавлено поле transition;
* BOBUH-18362 Удаление поля функция в BaseElectronicDocumentTransition и добавление function_pack;
* BOBUH-18362 Правки .gitignore;
* BOBUH-18362 В класс BaseElectronicDocumentTransition добавлены поля icon_class и info_text.

0.0.3

* Добавление внешнего ключа document в BaseElectronicDocumentEditingLog;
* Добавление базового прокси BaseElectronicDocumentEditingLogListProxy.

0.0.2

* Реализация базовых моделей;
* Добавление базовых компонентов;
* Добавление модели-перечисления для статуса электронной подписи.

0.0.1

* Инициализация проекта
* Добавление каркаса документации