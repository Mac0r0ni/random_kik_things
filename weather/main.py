        if chat_message.body.lower().startswith("weather "):
            mssg = chat_message.body.lower()
            get_weather = mssg.replace("weather ", "")
            area_code = get_weather
            api_url = "http://api.weatherstack.com/current?access_key=***API KEY GOES HERE***&query=" + area_code
            response = requests.get(api_url)
            weather_data = response.json()
            temperature_fahrenheit = (weather_data['current']['temperature'] * 9 / 5) + 32
            humidity = weather_data['current']['humidity']
            wind_speed = weather_data['current']['wind_speed']
            if temperature_fahrenheit <= 32:
                image_path = 'images/under32.jpg'
            elif temperature_fahrenheit <= 50:
                image_path = 'images/under50.jpg'
            elif temperature_fahrenheit <= 67:
                image_path = 'images/under67.jpg'
            elif temperature_fahrenheit <= 79:
                image_path = 'images/under79.jpg'
            else:
                image_path = 'images/over80.jpg'
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 50)
            message_parts = [f"Temperature: {temperature_fahrenheit} F"]
            if humidity is not None:
                message_parts.append(f"Humidity: {humidity}%")
            if wind_speed is not None:
                message_parts.append(f"Wind Speed: {wind_speed} mph")
            message = "\n".join(message_parts)
            text_width, text_height = draw.textsize(message, font)
            x = (image.width - text_width) / 2
            y = (image.height - text_height) / 2
            draw.text((x, y), message, font=font, fill=(0, 0, 0))
            image.save("weather.jpg")
            self.client.send_chat_image(chat_message.from_jid, "weather.jpg")
