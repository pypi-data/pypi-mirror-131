# Translate Middleware

The Translate Middleware library is a use to translate text using cognitive services translator.<BR>
Cognitive Services Translator is a cloud-based machine translation service you can to translate text in with a simple REST API call

## Installing

    pip install botbuilder-sangam-cognitive-text-translate

## Usage

All middleware is created and used in the same way. For example, import the `TranslateMiddleware` class from the package, and add it to your bot adapter:

    from botbuilder.sangam.cognitive.text.translate import TranslateMiddleware , TranslateSettings

    translate_settings = TranslateSettings()
    translate_settings.subscription_key = ''
    translate_settings.from_lang = 'en'
    translate_settings.to_lang = ['de','it','ta']
    translate_settings.subscription_region = ''

    adapter.use(TranslateMiddleware(translate_settings));

When used, the `turn_state` on the `TurnContext` will have a property named `translate_response`, which will be an return an TranslateResponse object.

Supported middleware classes include:

| Class | Property/Properties on `turn_state` |
| ---- | ----------- |
| `TranslateMiddleware` | `context.turn_state.get("translate_response")` |

# TranslateService
TranslateService is use to translate text using cognitive services translator without Middleware.
    
    from botbuilder.sangam.cognitive.text.translate import TranslateService , TranslateSettings ,TranslateResponse

    translate_settings = TranslateSettings()
    translate_settings.subscription_key = ''
    translate_settings.from_lang = 'en'
    translate_settings.to_lang = ['de','it','ta']
    translate_settings.subscription_region = ''
    
    
    //call the translate service 
    
    service = TranslateService(translate_settings)
    response = service.translate_text('hello')
    
