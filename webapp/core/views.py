from django.http import HttpResponseRedirect
from django.shortcuts import render
import tiktoken


def tiktoken_form(request):
    body = request.session.get('body') or ''
    tokens = request.session.get('tokens') or 0

    request.session.flush()

    template = 'tiktoken_form.html'

    return render(request, template, {
        "body": body,
        "tokens": tokens,
    })


def process_tiktoken(request):
    body = request.POST.get('body').strip()
    if not body:
        raise '403'

    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(body)

    print(tokens)
    request.session['body'] = body
    request.session['tokens'] = len(tokens)

    return HttpResponseRedirect('/')
