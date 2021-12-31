# NINES Flow

---
* Author: 이상현
* Maintainer: 이상현, 이권재

### Directory Tree

```bash
├── src
│   ├── flow
│   │   └── controller
│   │   └── handler
│   ├── db
│   ├── http
│   ├── model
│   ├── util
│   └── flow_manager.py
├── run.sh
└── main.sh
``` 

### Controller 추가시 주의사항
* 작성할 파일은 src.flow.controller 바로 밑에 두지 않는다.
    * 반드시 적당한 분류로 패키지 형태로 작성한다
    * ex) predict package
* 반드시 src.flow.controller의 Controller를 상속한다.
* flow script는 _run을 override하여 사용한다.
* package에서 공통적으로 사용하는 함수가 있다면 package __init__.py에 Controller를 상속하는 슈퍼클래스를 작성하고 그 클래스에 작성한 후 새로 작성하는 Controller에서 상속 받도록 한다.
* 코드 효율이나 정리를 위해 해당 클래스에서 단독으로 사용할 함수가 필요한 경우 해당 클래스에 작성 해준다.
* 일별로 돌아가는 flow의 경우 과거 flow를 다시 실행할 수 있도록 작성하길 권고.
    * 차후 nines_api를 통해 과거 flow를 다시 돌리는 기능을 개발할 예정
    * 그것을 위해 argument 기능을 만들어 놓음
* script 작성 후 따로 flow를 등록할 필요 없이 cron에만 등록하면 된다.

### Script Argument
* argument는 http request get에서 사용하는 url parameter와 유사하게 이용
* 값에 구분자 @를 사용하고 싶은 경우 Single quote(')로 감싸주면 된다.
  * ex) arg1=a@arg2='test@soulenergy.co.kr'@arg3=1234
```bash
run.sh flow_name arg1=1@arg2=2@arg3=3
```
