# Мир Кораблей

## Основные сущности

- **Board** — игровое поле 7×7, разделено по паттерну MVP:
  - `BoardModel` — данные и логика размещения
  - `BoardPresenter` — обработка ходов, смена фаз, проверка победы
  - `BoardViewQT` — отрисовка через PyQt5
- **Ship** — корабль с характеристиками (тип, HP, скорость, урон, команда)
- **Island** — остров (низкий — проходимый, высокий — блокирует линию огня)
- **Player** — игрок, владеет своими кораблями и выполняет атаки

## Используемые паттерны

| Паттерн   | Где применяется                                 |
|-----------|--------------------------------------------------|
| **MVP**   | Основная архитектура игры (Board, Ship)         |
| **Strategy** | Разные стратегии атаки для типов кораблей (`models/strategies/attack/`) |
| **Factory** | Создание кораблей с видом и колбэками (`factories/ship_factory.py`) |

## Структура проекта

```text
src/
├── constants/              # Константы и маппинг команд
├── core/                   # API игрового движка
├── data/
│   └── ships_data.json     # Конфигурация кораблей и флотов
├── factories/
│   └── ship_factory.py     # Создание кораблей
├── models/
│   ├── board_model.py
│   ├── ship.py
│   ├── player.py
│   ├── island.py
│   └── strategies/
│       └── attack_strategies.py            # Стратегии поиска целей (Destroyer, Cruiser+Battleship)
├── presenters/
│   └── board_presenter.py                  # Основная игровая логика
├── services/
│   └── ships_data_loader.py#               # Загрузка данных из JSON
├── utils/
│   ├── enums.py
│   ├── logger.py           # Логирование
│   ├── coords.py            
│   └── manhattan_distance.py
├── views/
│   ├── board_view.py       # базовый класс
│   ├── board_view_qt.py    # конкретная реализация BoardView на данном API
│   └── ship_view.py        # базовый класс
│   └── ship_view_qt.py     # конкретная реализация ShipView на данном API
├── game.py                 # Инициализация игры
└── main.py                 # Точка входа
