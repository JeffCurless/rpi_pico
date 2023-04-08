import json
import network
import time
import urequests


class chatGPT:
    """
        Description: This is a function to hit chat gpt API and get a
        response.
        
        Parameters:
        
        api_key[str]: API key for access
        max_tokens[int]: The maximum number of tokens to
            generate in the completion.
            
        Returns: Simply prints the response
    """
    def __init__( self, api_key, max_tokens ):
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + api_key}
        
    def askQuestion( self, prompt ):
        data    = {'model': 'text-davinci-003',
                   'prompt': prompt,
                   'max_tokens': self.max_tokens}
        r = urequests.post( 'https://api.openai.com/v1/completions',
                            json=data,
                            headers=self.headers)
        if r.status_code >= 300 or r.status_code < 200:
            print( "There was an error with your request\n" +
                   "Response Status: " + str(r.text))
        else:
            print("Success")
            response_data = json.loads(r.text)
            completion = response_data["choices"][0]["text"]
            print( completion )
        r.close()
