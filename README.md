Sequrity_monitor v 0.9

Программа для автоматического отслеживания чата безопасности вашего сообщества
в игре EVE-online.

Для работы репозитория достаточно применить pip install -r requirements.txt
после развертывания виртуальнгого окружения.

Суть выполняемой работы.
Программа по логфайлам игры отслеживает свездную систему персонажа, отслеживает 
чат безопвсности сообщества и если в чат была пролинкована система находящаяся
от персонажа не более чем в 10 джампах, всплывает пуш-уведомление со звуковым сигналом
и с информацией сколько потенциальному противнику джампов до системы в которой 
находится ваш персонаж.

Потенциально создав ехе файл, приложение можно запустить сколько раз сколько у вас
игровых персонажей, главное правильно заполнить информацию для отслеживания.

Для корректной работы программы после ее запуска необходимо:
1. В верхнем текстовом поле ввести ID вашего игрового персонажа.
2. В среднее текстовое поле ввести название чата в котороый линкуются нетральные персонажи
и системы в которых они находятся.
3. В нижнее текстовое поле нужно ввести название локального чата, если игра
использует русский язык название "Локальный" если английский "Local". Надежнее
будет посмотреть название в логах чата.
4. Нажатием на кнопку "Директория логов" выбрать папку куда игра сохраняет логи игры.
5. Нажатием на кнопки "Файл систем" загрузить актуальный файл с названиеями звездных
систем eve-online, находится в репозитории с программой.
6. После выбора нужных файлов и папок отслеживание можно запускать нажатием
на кнопку "Запустить мониторинг"
7. Остановить работу программы можно нажатием на кнопку "Остановить мониторинг"

