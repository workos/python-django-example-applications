import os
import workos
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.
workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)


def list_factors(request):
    if request.session.get("factor_list") == None:
        request.session["factor_list"] = []
        request.session["current_factor_qr"] = ""
        request.session["phone_number"] = ""

    if request.session.get("factor_list"):
        return render(
            request,
            "mfa/list_factors.html",
            {
                "factors": request.session.get("factor_list"),
            },
        )

    return render(request, "mfa/list_factors.html")


def enroll_factor_details(request):
    return render(request, "mfa/enroll_factor_details.html")


@csrf_exempt
def enroll_factor(request):
    factor_type = request.POST["type"]

    if factor_type == "sms":
        factor_type = "sms"
        phone_number = request.POST["phone_number"]
        new_factor = workos.client.mfa.enroll_factor(
            type=factor_type, phone_number=phone_number
        )
        if request.session.get("factor_list"):
            request.session["factor_list"].append(new_factor)
        else:
            request.session["factor_list"] = [new_factor]

    if factor_type == "totp":
        factor_type = "totp"
        totp_issuer = request.POST["totp_issuer"]
        totp_user = request.POST["totp_user"]
        new_factor = workos.client.mfa.enroll_factor(
            type=factor_type, totp_issuer=totp_issuer, totp_user=totp_user
        )
        if request.session.get("factor_list") != None:
            new_session_list = request.session["factor_list"]
            new_session_list.append(new_factor)
            request.session["factor_list"] = new_session_list
        else:
            request.session["factor_list"] = [new_factor]

    return redirect("list_factors")


def factor_detail(request):
    factorId = request.GET["id"]
    for factor in request.session["factor_list"]:
        if factor["id"] == factorId:
            fullFactor = factor

        phone_number = "-"
        if factor["type"] == "sms":
            phone_number = factor["sms"]["phone_number"]

        if factor["type"] == "totp":
            request.session["current_factor_qr"] = factor["totp"]["qr_code"]

    request.session["current_factor"] = fullFactor["id"]
    request.session["current_factor_type"] = fullFactor["type"]
    return render(
        request,
        "mfa/factor_detail.html",
        {
            "factor": fullFactor,
            "phone_number": phone_number,
            "qr_code": request.session["current_factor_qr"],
        },
    )


@csrf_exempt
def challenge_factor(request):
    if request.session["current_factor_type"] == "sms":
        message = request.POST["sms_message"]
        request.session["sms_message"] = message
        challenge = workos.client.mfa.challenge_factor(
            authentication_factor_id=request.session["current_factor"],
            sms_template=message,
        )

    if request.session["current_factor_type"] == "totp":
        authentication_factor_id = request.session["current_factor"]
        challenge = workos.client.mfa.challenge_factor(
            authentication_factor_id=authentication_factor_id,
        )
    request.session["challenge_id"] = challenge["id"]
    return render(request, "mfa/challenge_factor.html")


@csrf_exempt
def verify_factor(request):
    code = request.POST["code"]
    challenge_id = request.session["challenge_id"]
    verify_factor = workos.client.mfa.verify_factor(
        authentication_challenge_id=challenge_id,
        code=code,
    )
    challenge = verify_factor["challenge"]
    valid = verify_factor["valid"]
    type = request.session["current_factor_type"]

    return render(
        request,
        "mfa/verify_factor.html",
        {"challenge": challenge, "valid": valid, "type": type},
    )


def clear_session(request):
    request.session.clear()
    return redirect("list_factors")
