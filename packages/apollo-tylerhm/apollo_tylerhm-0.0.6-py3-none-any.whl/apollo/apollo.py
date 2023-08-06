import sys
from . import arguments, diff_checker, token_checker, epsilon_checker

def _cli():
    args = arguments.parse()
    with open(args.user_output) as user_out, open(args.judge_output) as judge_out:
        if args.tok:
            res = token_checker.check(user_out, judge_out)
        elif args.eps:
            res = epsilon_checker.check(user_out, judge_out, args.eps)
        else:
            res = diff_checker.check(user_out, judge_out)

        if (args.verbose):
            print(res.to_string())

        sys.exit(res.verdict.return_code);

def check(input, user_output, judge_output, tokenizer = False, epsilon = None):
    with open(user_output) as user_out, open(judge_output) as judge_out:
        if tokenizer:
            res = token_checker.check(user_out, judge_out)
        elif epsilon != None:
            res = epsilon_checker.check(user_out, judge_out, epsilon)
        else:
            res = diff_checker.check(user_out, judge_out)

    return res.to_JSON()
