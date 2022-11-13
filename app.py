from flask import Flask, request
import bs4
from scanner import *
# Jsonify? https://growingsaja.tistory.com/299

app = Flask(__name__)

# Welcome, you are now connected to log-streaming service.

@app.route('/')
def hello_world():
    return 'Hello, World!'

#  === getMEAL ===
@app.route('/api/getMeal', methods=['POST'])
def getMeal():
    body = request.get_json()
    print(f"[수신] BODY: {body}")
    print(f"[수신] Parameters: {body['action']['params']}")
    print(f"[수신] 대화내용: {body['userRequest']['utterance']}")
    try: 
        day = body['action']['params']['sys_date']  # 기본값이 'today'가 전달된다면 [dateTag]가 없으므로 에러 발생
    except Exception as e: print(f"[수신] 오류: {e}"); day = 'today'
        
    if day == 'today':  # 예상치 못했던 부분이라 원래 코드 수정하는 대신 한글화
        day = '오늘'
    else:
        day = day.split()[3].replace("\"", "").replace(",","")
        if day == 'tomorrow': day = '내일'
        elif day == 'Monday': day = '월'
        elif day == 'Tuesday': day = '화'
        elif day == 'Wednesday': day = '수'
        elif day == 'Thursday': day = '목'
        elif day == 'Friday': day = '금'
        elif day == 'Saturday': day = '토'
        elif day == 'Sunday': day = '일'
            
    print(f"[수신] 요청날짜: {day}")
    try: campusName = body['action']['params']['campusName']
    except Exception as e: print(f"[수신] 오류: {e}"); campusName = '가좌캠퍼스'
    restaurantName = body['action']['params']['restaurantName']
    response = findMeal(urlSelector(campusName, restaurantName), restaurantName, day)
    if restaurantName == '중앙1식당' or restaurantName == '교육문화1층식당' or restaurantName == '가좌 교직원식당' or restaurantName == '가좌 생활관 식당': blockid = '636cee971a94d93e86de3ecb'  # 가좌 메인메뉴
    elif restaurantName == '칠암 학생식당' or restaurantName == '칠암 교직원식당' or restaurantName == '칠암 제1생활관 식당' or restaurantName == '칠암 제2생활관 식당': blockid = '636cf0041a94d93e86de3ed4'  # 칠암 메인메뉴
    elif restaurantName == '통영 학생식당' or restaurantName == '통영 교직원식당' or restaurantName == '통영 생활관 식당': blockid = '636cf02f3236e276c315bdf3'  # 통영 메인메뉴
    else: blockid = '636c6383a197ae433d32dee0'  # 기본 메인메뉴
    print(f"[송신] 블록ID: {blockid}")
    print(f"restaurantName: {restaurantName}")
    print(f"response[1]: {response[1]}")
    if response[1] == True:  # 학식을 찾았을 경우에 대한 응답 JSON
        if restaurantName == '중앙1식당':  # Optimized for 중앙1식당
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                    {
                        "simpleText": {
                                            "text": response[0]
                                        }
                    },
                    {
                        "carousel": {
                        "type": "listCard",
                        "items": [
                            {
                            "header": {
                                "title": "[고정메뉴 09:00~18:00] (1/2)"
                            },
                            "items": [
                                {
                                "title": "중앙김밥",
                                "description": "1,500원",
                                },
                                {
                                "title": "땡초, 치즈, 참치김밥",
                                "description": "2,000원",
                                },
                                {
                                "title": "참치치즈, 땡초치즈, 땡초참치김밥",
                                "description": "2,500원",
                                }
                            ]
                            },
                            {
                            "header": {
                                "title": "[고정메뉴 09:00~18:00] (2/2)"
                            },
                            "items": [
                                {
                                "title": "중앙라면",
                                "description": "2,000원",
                                },
                                {
                                "title": "치즈, 땡초, 만두라면",
                                "description": "2,500원",
                                },
                                {
                                "title": "공기밥",
                                "description": "500원",
                                }
                            ]
                            }
                        ]
                        },
                        
                    },
                    
                    ],
                    "quickReplies": [
                        {   # https://devtalk.kakao.com/t/id/112787
                            "action": "block",
                            "blockId": blockid,
                            "label": "처음으로 돌아가기 🏠"
                        },
                        {
                            "messageText": "내일 " + restaurantName,
                            "action": "message",
                            "label": "내일은?"
                        },
                        {
                            "messageText": "월요일 " + restaurantName,
                            "action": "message",
                            "label": "월"
                        },
                        {
                            "messageText": "화요일 " + restaurantName,
                            "action": "message",
                            "label": "화"
                        },
                        {
                            "messageText": "수요일 " + restaurantName,
                            "action": "message",
                            "label": "수"
                        },
                        {
                            "messageText": "목요일 " + restaurantName,
                            "action": "message",
                            "label": "목"
                        },
                        {
                            "messageText": "금요일 " + restaurantName,
                            "action": "message",
                            "label": "금"
                        }
                    ]
                }
                }
        elif restaurantName == '교육문화1층식당':  # Optimized for 교육문화1층식당
            print(f"[정보] 교육문화1층식당 response")
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                    {
                        "simpleText": {
                                            "text": response[0]
                                        }
                    }
                    ],
                    "quickReplies": [
                        {   # https://devtalk.kakao.com/t/id/112787
                            "action": "block",
                            "blockId": blockid,
                            "label": "처음으로 돌아가기 🏠"
                        },
                        {
                            "messageText": "내일 " + restaurantName,
                            "action": "message",
                            "label": "내일은?"
                        },
                        {
                            "messageText": "월요일 " + restaurantName,
                            "action": "message",
                            "label": "월"
                        },
                        {
                            "messageText": "화요일 " + restaurantName,
                            "action": "message",
                            "label": "화"
                        },
                        {
                            "messageText": "수요일 " + restaurantName,
                            "action": "message",
                            "label": "수"
                        },
                        {
                            "messageText": "목요일 " + restaurantName,
                            "action": "message",
                            "label": "목"
                        },
                        {
                            "messageText": "금요일 " + restaurantName,
                            "action": "message",
                            "label": "금"
                        }
                    ]
                }
                }
        elif restaurantName == '가좌 교직원식당':  # Optimized for 가좌 교직원식당
            print(f"[정보] 가좌 교직원식당 response")
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [
                    {
                        "simpleText": {
                                            "text": response[0]
                                        }
                    }
                    ],
                    "quickReplies": [
                        {   # https://devtalk.kakao.com/t/id/112787
                            "action": "block",
                            "blockId": blockid,
                            "label": "처음으로 돌아가기 🏠"
                        },
                        {
                            "messageText": "내일 " + restaurantName,
                            "action": "message",
                            "label": "내일은?"
                        },
                        {
                            "messageText": "월요일 " + restaurantName,
                            "action": "message",
                            "label": "월"
                        },
                        {
                            "messageText": "화요일 " + restaurantName,
                            "action": "message",
                            "label": "화"
                        },
                        {
                            "messageText": "수요일 " + restaurantName,
                            "action": "message",
                            "label": "수"
                        },
                        {
                            "messageText": "목요일 " + restaurantName,
                            "action": "message",
                            "label": "목"
                        },
                        {
                            "messageText": "금요일 " + restaurantName,
                            "action": "message",
                            "label": "금"
                        }
                    ]
                }
                }
            return responseBody
        if restaurantName == '가좌 생활관 식당':  # Optimized for 아람관
            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": response[0],
                    "quickReplies": [
                        {   # https://devtalk.kakao.com/t/id/112787
                            "action": "block",
                            "blockId": blockid,
                            "label": "처음으로 돌아가기 🏠"
                        },
                        {
                            "messageText": "내일 " + restaurantName,
                            "action": "message",
                            "label": "내일은?"
                        },
                        {
                            "messageText": "월요일 " + restaurantName,
                            "action": "message",
                            "label": "월"
                        },
                        {
                            "messageText": "화요일 " + restaurantName,
                            "action": "message",
                            "label": "화"
                        },
                        {
                            "messageText": "수요일 " + restaurantName,
                            "action": "message",
                            "label": "수"
                        },
                        {
                            "messageText": "목요일 " + restaurantName,
                            "action": "message",
                            "label": "목"
                        },
                        {
                            "messageText": "금요일 " + restaurantName,
                            "action": "message",
                            "label": "금"
                        }
                    ]
                }
                }
            print(f"[정보] responseBody: {responseBody}")
            print("[정보] 가좌 생활관 식당 responseBody SEND")
            return responseBody
    if response[1] == False:  # 학식을 찾지 못했을 경우에 대한 응답 JSON
        responseBody = {  # TODO 내일의 학식을 받은 상태에서 그 날의 내일. 즉, 모레의 학식도 받을 수 있도록 수정
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": response[0]
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "action": "block",
                        "blockId": blockid,
                        "label": "처음으로 돌아가기 🏠"
                    },
                    {
                        "messageText": "내일 " + restaurantName,
                        "action": "message",
                        "label": "내일은?"
                    },
                    {
                        "messageText": "월요일 " + restaurantName,
                        "action": "message",
                        "label": "월"
                    },
                    {
                        "messageText": "화요일 " + restaurantName,
                        "action": "message",
                        "label": "화"
                    },
                    {
                        "messageText": "수요일 " + restaurantName,
                        "action": "message",
                        "label": "수"
                    },
                    {
                        "messageText": "목요일 " + restaurantName,
                        "action": "message",
                        "label": "목"
                    },
                    {
                        "messageText": "금요일 " + restaurantName,
                        "action": "message",
                        "label": "금"
                    }
                ]
            }
        }
    else:
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "에러가 발생했습니다."
                        }
                    }
                ]
            }
        }
    if restaurantName == "??":
        pass
    else:
        pass

















    return responseBody





## 학교 뉴스 크롤링
@app.route('/api/getNews', methods=['POST'])
def getNews():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])
    response = findNews()
    
    responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": response[0]
                }
                }

    return responseBody




















@app.route('/api/TEST', methods=['POST'])
def TEST():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "basicCard": {
          "title": "보물상자",
          "description": "보물상자 안에는 뭐가 있을까",
          "thumbnail": {
            "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/lj3JUcmrzC53YIjNDkqbWK.jpg"
          },
          "profile": {
            "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4BJ9LU4Ikr_EvZLmijfcjzQKMRCJ2bO3A8SVKNuQ78zu2KOqM",
            "nickname": "보물상자"
          },
          "social": {
            "like": 1238,
            "comment": 8,
            "share": 780
          },
          "buttons": [
            {
              "action": "message",
              "label": "열어보기",
              "messageText": "짜잔! 우리가 찾던 보물입니다"
            },
            {
              "action":  "webLink",
              "label": "구경하기",
              "webLinkUrl": "https://e.kakao.com/t/hello-ryan" # <- urlselector
            }
          ]
        }
      }
    ]
  }
}

    return responseBody







## 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


@app.route('/api/getMenu', methods=['POST'])  # gnurang.azurewebsites.net/api/getMenu로 POST 할 경우 여기로 들어옴
def getMenu():  # id, campus, restaurant, date # 여기다가 매개변수 넣을 수 있는지 잘 모르겠음.
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])
    # 엔티티를 캠퍼스 이름에 맞춰서 다르게 만들어 줘야할것 같은데...? 모아 놓으니 if문이 너무 길어질것 같음
    # 일단 귀찮으니 킵고잉.
    # id 별로 개인화 추가예정, id는 body['userRequest']['user']['id']로 가져올 수 있음. (copilot)
    # id를 데이트베이스에 저장하고, 저장된 id에 맞는 캠퍼스를 가져오는 방식으로 개인화 가능할듯.
    # 하지만 난, DB를 써본적이 없지.. ㅎ
    # 그냥 캠퍼스 이름을 각각 엔티티로 만들어서, 그 엔티티를 가져오는 방식으로 개인화를 하는것도 나쁘진 않을듯.

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "This is Simple Alt Text Message"
                    }
                }
            ]
        }
    }

    return responseBody

# def findMenu(campus, restaurant, date):
#     web = requests.get('https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=2168&menuCd=DOM_0000001000000000010')
#     bs4Web = bs4.BeautifulSoup(web.text, 'html.parser')
    
    
    
#     return menu

