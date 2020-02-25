
import re, json, base64, string

input_event = 'event_data.txt'
output_event = 'event_next.txt'

def publish_event(d):
    # Creates the updated event.
    # Input is the enhanced dictionary
    
    with open(output_event, "w+") as fo:
        last_key = list(d.keys())[-1] # in recent 3.8 dictionaries are ordered! 
        # Otherwise use some counter to tell if on last element
        
        for k, v in d.items():
            #  Req. preserve the original output
            # last field has got no trailing space but a new line?.
            out = '{0}: \"{1}\" '.format(k, v) if k != last_key else '{0}: \"{1}\"\n'.format(k, v)
            fo.write(out)
        
    

with open(input_event) as fd:
    data = fd.read()
    
    # use Regex for the heavy lifting as long as we could derive a decent rule
    # Key non blank(+) ID (non colon) followed by colon is [^:]+:, do not capture colon
    # do not capture space and leading quote (cosmetics only)
    # Value (* can them be blank?) is made of any number of escaped quotes \\" or non-quotes [^"]
    # do not capture trailing quotes and possible new lines
    p = re.compile(r'([^:]+): "((?:\\"|[^"])*)"\s*\n*')    
    d = dict(p.findall(data))
    
    jsonTextEvent = json.dumps(d, indent = 2)    
    # print(jsonTextEvent)
    
    hint = d["hint"]
    
    print ("hint =", hint)    
    # hint is all ASCII upper and lower case.
    # hash and encryption tend to create binary data. Chances are this is an ASCII armor format.
    # 
    # Ideally run it through a set of known filters to determine exact format.
    # 1st manual test reveals is the base64 of "XOR with 0x17F".
    print ("Guideline: ", base64.b64decode(hint).decode("ascii"))
    
    # XOR is associative operation, i.e. (A xor B) xor B = A xor (B xor B) = A xor 0x0000 = A
    # so apply the hint to the currently listed values to derive the original input:
    # d["one"]   0x154 xor 0x17F = 0x2B = 43
    # d["two"]   0x150 xor 0x17F = 0x2F = 47
    # d["three"] 0x14A xor 0x17F = 0x35 = 53
    # d["four"]  0x144 xor 0x17F = 0x3B = 59
    # These are consecutive prime numbers (14th), so the solution to the puzzle is 61
    # (use a dedicated library to find the n-th prime number considering the above offset)
    
    # build the output event
    d["five"] = "0x%X" % (61 ^ 0x17F)
    print ("Solution is:", d["five"])
    
    publish_event(d)
