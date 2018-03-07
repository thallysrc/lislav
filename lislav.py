import math
import operator as op

Symbol = str
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)
Env    = dict

def standard_env() -> Env:
    "An environment with some scheme standard procedures"
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        '>':op.gt, '>':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs':abs,
        'append':op.add,
        'apply':lambda proc, args: proc(*args),
        'begin':lambda *x: x[-1],
        'car':lambda x: x[0],
        'cdr':lambda x: x[1:],
        'cons':lambda x,y: [x] + y,
        'eq?':op.is_,
        'expt':pow,
        'equal?':op.eq,
        'length':len,
        'list':lambda *x: List(x),
        'list?':lambda x: isinstance(x, List),
        'map':map,
        'max':max,
        'min':min,
        'not':op.not_,
        'null?':lambda x: x == [],
        'number?':lambda x: isinstance(x, Number),
        'print':print,
        'procedure?':callable,
        'round':round,
        'symbol?':lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

def eval(x: Exp, env=global_env) -> Exp:
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol): # variable reference
        return env[x]
    elif not isinstance(x, List): # constant number
        return x
    elif x[0] == 'if': # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define': # definition
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:  # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def tokenize(chars: str) -> list:
    "convert a string of characters into a list of tokens"
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
    "Read a scheme expression from a string"
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list) -> Exp:
    "Read an expression from a sequence of tokens"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol"
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

program = "(begin (define r 10) (* pi (* r r)))"
print(eval(parse(program)))
