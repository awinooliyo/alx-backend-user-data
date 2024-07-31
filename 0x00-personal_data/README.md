# 0x00. Personal data

## Examples of Personally Identifiable Information (PII)

Personally Identifiable Information (PII) refers to any data that can identify a specific individual. Examples include:
- Full name
- Social Security Number (SSN)
- Email address
- Phone number
- Date of birth
- Physical address
- Passport number
- Driver’s license number

## How to Implement a Log Filter that Will Obfuscate PII Fields

To protect PII in log files, you can implement a log filter that obfuscates these fields. Below is an example using Python with the `logging` module:

```python
import logging
import re

class PIIObfuscatingFilter(logging.Filter):
    def filter(self, record):
        record.msg = self.obfuscate_pii(record.msg)
        return True
    
    def obfuscate_pii(self, message):
        # Example patterns for email and SSN
        patterns = {
            'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b'
        }
        
        for key, pattern in patterns.items():
            message = re.sub(pattern, f'[OBFUSCATED {key.upper()}]', message)
        
        return message

# Configure logging
logger = logging.getLogger('my_logger')
logger.addFilter(PIIObfuscatingFilter())
logger.setLevel(logging.DEBUG)

# Example usage
logger.info('User email: john.doe@example.com, SSN: 123-45-6789')
