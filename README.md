# xmlgenerator

Генерация xml из xsd

## Как запустить

### Установить зависимости

> python3 -m venv venv  
> source venv/bin/activate  
> pip install -r requirements.txt

## Запуск скрипта

> python xmlfromxsd.py [-h] [-s SRC-DIR] [-t TARGET-DIR] -f FILE


Парамеетры:  
<dl>
  <dt>-h, --help</dt>
  <dd>показать справку и выйти .</dd>
 
  <dt>-s SRC-DIR, --srcdir SRC-DIR</dt>
  <dd>папка с исходным файлом (по умолчанию data)
  </dd>
  
  <dt>-t TARGET-DIR, --targetdir TARGET-DIR </dt>
  <dd> папка для результата (по умолчанию совпадает с исходной), при отсутствии папки, она будет создана. 
  </dd>
  <dt>-f FILE, --file FILE</dt>
    <dd>файл со схемой
    </dd>
  <dt>-c COUNT, --count COUNT</dt>
    <dd>Количество генерируемых документов. По умолчанию 1. 
    </dd>
</dl>
