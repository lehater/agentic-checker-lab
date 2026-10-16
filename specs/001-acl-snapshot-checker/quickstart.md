# Quickstart — будущая независимая проверка реализации

**Status:** Verification guide only. Программа ещё не реализована, команды ниже не запускались.

## Preconditions
- Python 3.12+.
- RPG создал исполняемый модуль `acl_checker` согласно CLI-контракту.
- Создан файл `fixtures/example.json` с входными данными из [contracts/cli.md](contracts/cli.md).

## End-to-end run (после реализации)
```bash
python -m acl_checker fixtures/example.json > actual.json
python -m json.tool actual.json
```
Ожидается exit 0, два совпадения (R10 deny и R20 permit) в этом порядке, одно устройство/один ACL, `matched_rule_count=2`, без глобального verdict.

## Additional acceptance checks
1. Изменить `source_ip` за пределы CIDR первого правила: R10 не совпадает, R20 остаётся.
2. Указать порт назначения 444: в данном fixture оба правила перестают совпадать.
3. Создать два ACL на одном устройстве: результат содержит два отдельных ACL-группы.
4. Удалить snapshot, оставив ссылку в relevant_acls: exit 2; diagnostic stderr; no partial stdout report.
5. Добавить неизвестный протокол/invalid prefix: exit 2.
6. Создать fixture без relevant_acls: exit 0, пустая коллекция устройств и zero matched count.
7. Изменить порядок правил в snapshot: соответствующий порядок matches должен измениться.
8. Повторить одинаковый fixture: JSON семантически эквивалентен между запусками.

## Test ownership and traceability
Разработчик или независимый тестировщик реализует эти проверки, трассируя их к FR-001..013. Этот документ не является доказательством выполнения тестов; будущий test suite/CI — отдельная стадия. Предметные ожидаемые результаты должны быть зафиксированы до запуска RPG.
