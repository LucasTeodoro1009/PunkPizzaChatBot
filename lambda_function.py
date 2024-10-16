import urllib3
import json

http = urllib3.PoolManager()

def lambda_handler(event, context):
    tts_api_url = "https://ry3rbapgk0.execute-api.us-east-1.amazonaws.com/dev/v1/tts"
    slack_webhook_url = "https://hooks.slack.com/services/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"
    
    # Capturar o nome da intent
    intent_name = event['sessionState']['intent']['name']
    print("Intent Name: ", intent_name)
    
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "Failed",
                "slots": event['sessionState']['intent']['slots']
            }
        }
    }

    if intent_name == 'PizzaOrder':
        # Capturar os slots
        slots = event['sessionState']['intent']['slots']
        print("Slots: ", slots)
        
        pizza_size = slots.get('PizzaSize', {}).get('value', {}).get('interpretedValue', '')
        pizza_type = slots.get('PizzaFlavor', {}).get('value', {}).get('interpretedValue', '')
        payment_method = slots.get('PaymentMethod', {}).get('value', {}).get('interpretedValue', '')
        address = slots.get('Address', {}).get('value', {}).get('interpretedValue', '')
        
        # Caso todos os slots sejam preenchidos
        if (pizza_size, pizza_type, payment_method, address):
            message = "Thanks for purchasing a %s %s pizza on PunkPizza! Your order is coming for %s in 40 minutes! Please, have the %s in your hands to make the payment on delivery." % (pizza_size, pizza_type, address, payment_method)
            print("Mensagem completa a ser convertida pela API TTS: ", message)
            
            tts_payload = {
                "phrase": message
            }
            encoded_tts_payload = json.dumps(tts_payload).encode('utf-8')
            
            # Enviar a mensagem para a API
            tts_response = http.request(
                'POST',
                tts_api_url,
                body=encoded_tts_payload,
                headers={'Content-Type': 'application/json'}
            )
            
            tts_response_data = json.loads(tts_response.data.decode('utf-8'))
            audio_url = tts_response_data['url_to_audio']
            
            # Estruturar botão do Slack
            slack_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Click to generate confirmation in audio format"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Play audio"
                            },
                            "url": audio_url,
                            "action_id": "button-action"
                        }
                    }
                ]
            }
            encoded_slack_message = json.dumps(slack_message).encode('utf-8')
            
            # Enviar a mensagem para o Slack
            slack_response = http.request(
                'POST',
                slack_webhook_url,
                body=encoded_slack_message,
                headers={'Content-Type': 'application/json'}
            )
            print("Resposta do Slack: ", slack_response.status)
            
    elif intent_name == 'BurgerOrder':
        # Capturar os slots
        slots = event['sessionState']['intent']['slots']
        print("Slots: ", slots)
        
        burger_type = slots.get('BurgerFlavor', {}).get('value', {}).get('interpretedValue', '')
        steak_point = slots.get('SteakDoneness', {}).get('value', {}).get('interpretedValue', '')
        payment_method = slots.get('PaymentMethod', {}).get('value', {}).get('interpretedValue', '')
        address = slots.get('Address', {}).get('value', {}).get('interpretedValue', '')
        
        # Caso todos os slots sejam preenchidos
        if (burger_type, steak_point, payment_method, address):
            message = "Thanks for purchasing a %s burger on PunkPizza! Your order is coming for %s in 40 minutes! Please, have the %s in your hands to make the payment on delivery." % (burger_type, address, payment_method)
            print("Mensagem completa a ser convertida pela API TTS: ", message)
            
            tts_payload = {
                "phrase": message
            }
            encoded_tts_payload = json.dumps(tts_payload).encode('utf-8')
            
            # Enviar a mensagem para a API
            tts_response = http.request(
                'POST',
                tts_api_url,
                body=encoded_tts_payload,
                headers={'Content-Type': 'application/json'}
            )
            
            tts_response_data = json.loads(tts_response.data.decode('utf-8'))
            audio_url = tts_response_data['url_to_audio']
            
            # Estruturar botão do Slack
            slack_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Click to generate confirmation in audio format"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Play audio"
                            },
                            "url": audio_url,
                            "action_id": "button-action"
                        }
                    }
                ]
            }
            encoded_slack_message = json.dumps(slack_message).encode('utf-8')
            
            # Enviar a mensagem para o Slack
            slack_response = http.request(
                'POST',
                slack_webhook_url,
                body=encoded_slack_message,
                headers={'Content-Type': 'application/json'}
            )
            print("Resposta do Slack: ", slack_response.status)

    elif intent_name == 'DessertOrder':
        # Capturar os slots
        slots = event['sessionState']['intent']['slots']
        print("Slots: ", slots)
        
        dessert = slots.get('Dessert', {}).get('value', {}).get('interpretedValue', '')
        payment_method = slots.get('PaymentMethod', {}).get('value', {}).get('interpretedValue', '')
        address = slots.get('Address', {}).get('value', {}).get('interpretedValue', '')
        
        # Caso todos os slots sejam preenchidos
        if (dessert, payment_method, address):
            message = "Thanks for purchasing a %s on PunkPizza! Your order is coming for %s in 40 minutes! Please, have the %s in your hands to make the payment on delivery." % (dessert, address, payment_method)
            print("Mensagem completa a ser convertida pela API TTS: ", message)
            
            tts_payload = {
                "phrase": message
            }
            encoded_tts_payload = json.dumps(tts_payload).encode('utf-8')
            
            # Enviar a mensagem para a API
            tts_response = http.request(
                'POST',
                tts_api_url,
                body=encoded_tts_payload,
                headers={'Content-Type': 'application/json'}
            )
            
            tts_response_data = json.loads(tts_response.data.decode('utf-8'))
            audio_url = tts_response_data['url_to_audio']
            
            # Estruturar botão do Slack
            slack_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Click to generate confirmation in audio format"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Play audio"
                            },
                            "url": audio_url,
                            "action_id": "button-action"
                        }
                    }
                ]
            }
            encoded_slack_message = json.dumps(slack_message).encode('utf-8')
            
            # Enviar a mensagem para o Slack
            slack_response = http.request(
                'POST',
                slack_webhook_url,
                body=encoded_slack_message,
                headers={'Content-Type': 'application/json'}
            )
            print("Resposta do Slack: ", slack_response.status)
    # Delegar a intent    
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "InProgress",
                "slots": event['sessionState']['intent']['slots']
            }
        }
    }

    return response
