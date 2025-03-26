from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import DesignedPrompt
import tiktoken
from .query_chain import query_pattern1


def index(request):
    return render(request, "index.html")


def templates(request):
    _templates = DesignedPrompt.objects.all()

    return render(request, "templates.html", {
        "templates": _templates,
    })


def execute_query(request, slug: str = None, ):
    template = DesignedPrompt.objects.filter(slug=slug)
    if not slug:
        raise Http404("slug is missing.")

    if not template.exists():
        raise Http404("prompt template not found.")

    if request.method == "POST":
        t = template[0]
        d = {}

        for key in t.input_keys:
            d[key] = request.POST.get(key)

        results: [str, str] = query_pattern1(t, d)
        request.session['answer0'] = results[0]
        request.session['answer1'] = results[1]
        request.session['dish'] = request.POST.get('dish')

        return HttpResponseRedirect(reverse("execute_query", args=[slug]))
    else:
        answer0 = request.session.get('answer0') or ''
        answer1 = request.session.get('answer1') or ''
        dish = request.session.get('dish') or ''

        request.session.flush()

        return render(
            request,
            "execute_query.html",
            {
                "dish": dish,
                "answer0": answer0,
                "answer1": answer1,
                "template": template[0],
                "input_keys": {"items": template[0].input_keys}
            }
        )


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

    return HttpResponseRedirect(reverse("tiktoken_form"))
