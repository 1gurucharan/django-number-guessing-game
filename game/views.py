import random
from django.shortcuts import render

def index(request):

    message = ""
    attempts_left = 7

    # Start game when range submitted
    if request.method == "POST":

        # START GAME
        if "start_game" in request.POST:
            low = int(request.POST.get("low"))
            high = int(request.POST.get("high"))

            request.session['low'] = low
            request.session['high'] = high
            request.session['number'] = random.randint(low, high)
            request.session['guess_count'] = 0

            message = "Game Started! Start guessing."

        # GUESS NUMBER
        elif "guess_submit" in request.POST:

            guess = int(request.POST.get("guess"))
            num = request.session['number']

            request.session['guess_count'] += 1
            gc = request.session['guess_count']

            attempts_left = 7 - gc

            if guess == num:
                message = f"🎉 Correct! Number was {num}"
                request.session.flush()

            elif gc >= 7:
                message = f"❌ Game Over! Number was {num}"
                request.session.flush()

            elif guess > num:
                message = "⬇ Too High! Try lower."

            else:
                message = "⬆ Too Low! Try higher."

    else:
        # default attempts
        if 'guess_count' in request.session:
            attempts_left = 7 - request.session['guess_count']

    return render(request, "game/index.html", {
        "message": message,
        "attempts_left": attempts_left,
        "game_started": 'number' in request.session
    })