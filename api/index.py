"""
Ultra-minimal Vercel function - no FastAPI, just basic HTTP
Testing if the Python runtime itself works
"""

def handler(request):
    """Ultra simple Vercel handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message": "Ultra minimal handler working", "status": "success", "test": "basic python function"}'
    }
