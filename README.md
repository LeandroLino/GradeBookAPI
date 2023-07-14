# Titulo

GradeBookAPI, projeto de gestão de professor, notas, alunos e disciplinas

## Instalação

Como faz para instalar o e caso seja necessário rodar o projeto localmente

```python
pip install -r requirements
```
```python
python3 manage.py migrate --run-syncdb
```
```python
python3 manage.py runserver

```
## Utilização
Uma API de controle estudantil, é possivel controlar alunos, professor, disciplinas e notas.

##POST /api/student/register/ - Criando uma conta de estudante:
```
{
  "username": "admin",
  "password": "1234"
}
```
**RESPONSE STATUS -> HTTP 200**
```
{
	"access_token": "<TOKEN DE AUTENTICAÇAO JWT>"
}
```

##POST /api/student/login/: - Logando como um estudante
```
{
{
  "email": "joedoe@gmail.com",
  "password": "123456"
}
```
**RESPONSE STATUS -> HTTP 200**
```
{
	"access_token": "<TOKEN DE AUTENTICAÇAO JWT ESTUDANTE>"
}
```

## POST /api/student/list-disciplines/<student_id>/ - Listando disciplina de um estudante:
**Header -> Authorization: Bearer <TOKEN-JWT>**
```
{
}
```
**RESPONSE STATUS -> HTTP 201**
```
[
	{
		"id": 1,
		"name": "Matematica",
		"workload": "80",
		"students": [
			{
				"id": 1,
				"name": "Aluno",
				"email": "JoeDoe@gmail.com",
				"registration": "7145632"
			}
		],
		"teachers": [
			{
				"id": 1,
				"name": "Professor",
				"email": "Joedoe@gmail.com",
				"inactive": false
			}
		]
	},
```
## GET '/api/student/list/student/<student_id>/discipline/<discipline_id>/' - Pega os boletins de um estudante dentro de uma disciplina
**Header -> Authorization: Bearer <TOKEN-JWT-STUDENT>**
**RESPONSE STATUS -> HTTP 200**
```
[
	{
		"id": 2,
		"delivery_date": "2023-08-16T00:00:00Z",
		"student": 1,
		"notes": [
			{
				"id": 1,
				"note": "10.00",
				"discipline": 2,
				"registration": "7145632"
			}
		]
	}
]
```
##GET /api/student/list/ - Lista todos os estudante:
```
{}
```
**RESPONSE STATUS -> HTTP 200**
```
[
	{
		"id": 1,
		"name": "Aluno",
		"email": "joedoe@gmail.com",
		"registration": "7145632",
		"disciplines": [],
		"inactive": false
	}
]
```

## POST /api/teacher/register/ - Registrando professor
```
{
  "name": "Professor",
  "email": "joe.doe@gmail.com",
  "password": "123456"
}

```
**RESPONSE STATUS -> HTTP 200**
```
{
	"access_token": "<TOKEN DE AUTENTICAÇAO JWT TEACHER>"
}
```

##POST /api/teacher/login/ - Login de professor
```
{
  "email": "joe.doe@gmail.com",
  "password": "123456"
}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"access_token": "<TOKEN DE AUTENTICAÇAO JWT TEACHER>"
}
```

##GET /api/teacher/list-disciplines/<teacher_id>/ - Listar disciplinas do professor
**Header -> Authorization: Token <token-do-professor>**
```
{}
```
**RESPONSE STATUS -> HTTP 201**
```
[
	{
		"id": 1,
		"name": "Matematica",
		"workload": "80",
		"students": [
			{
				"id": 1,
				"name": "Aluno",
				"email": "joedoe@gmail.com",
				"registration": "7145632"
			}
		],
		"teachers": [
			{
				"id": 1,
				"name": "Professor",
				"email": "joedoe@gmail.com",
				"inactive": false
			}
		]
	}...
```

##POST /api/disciplines/create/ - Criar disciplinas
**Header -> Authorization: Token <token-do-professor>**
```
{
  "name": "Matemaastica",
  "workload": 80
}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"id": 1,
	"name": "Matematica
	"workload": "80",
	"students": [],
	"teachers": [
		{
			"id": 1,
			"name": "Professor",
			"email": "jowdoe@gmail.com",
			"inactive": false
		}
	]
}
```

##GET /api/disciplines/list/discipline/<discipline_id>/ - Lista um disciplinas
**Header -> Authorization: Token <token-do-professor>**
```
{}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"id": 1,
	"name": "Matematica
	"workload": "80",
	"students": [],
	"teachers": [
		{
			"id": 1,
			"name": "Professor",
			"email": "jowdoe@gmail.com",
			"inactive": false
		}
	]
}
```


##GET /api/student/enroll/discipline/<discipline_id>/student/<student_id>/ - Matricula um estudante em uma disciplina
**Header -> Authorization: Token <token-do-professor>**
```
{}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"id": 1,
	"name": "Aluno",
	"email": "leao.lino@gmail.com",
	"registration": "7145632",
	"disciplines": [
		{
			"id": 1,
			"name": "Matematica",
			"workload": "80"
		}
	],
	"inactive": false
}
```

##POST /api/report-notes/create/discipline/<discipline_id>/student/<student_id>/ - Criar uma nota e atribui um estundante
Nesse endpoint foi feito uma adaptação no front juntando o endpoint de criar boletim com o de criar nota

**Header -> Authorization: Token <token-do-professor>**
```
{"note": "10.00"}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"id": 3,
	"note": "10.00",
	"discipline": 1,
	"registration": "7145632"
}
```

##POST /api/report-cards/create/student/<student_id>/note/<note_id>/ - Criar um boletim baseado em uma note existente
Nesse endpoint foi feito uma adaptação no front juntando o endpoint de criar boletim com o de criar nota

**Header -> Authorization: Token <token-do-professor>**
```
{"note": "10.00"}
```
**RESPONSE STATUS -> HTTP 201**
```
{
	"id": 2,
	"delivery_date": "2023-08-16",
	"student": 1,
	"notes": [
		{
			"id": 1,
			"note": "10.00",
			"discipline": 2,
			"registration": "7145632"
		}
	]
}
```
