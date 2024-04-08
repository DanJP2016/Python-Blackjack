from random import shuffle

# dealer stands on 17 or greater

deck_size = 52
max_decks = 1
total_deck_size = deck_size * max_decks
shoe = []

cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# map the cards to values
# ace can be 11 or 1
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11
}


player = {
    "cards": [],
    "total": 0,
    "stand": False
}


dealer = {
    "cards": [],
    "total": 0,
}


# takes the deck shoe, fills shoe with appropriate number of cards
def build_shoe(s):
    while len(s) < total_deck_size:
       for x in cards:
           s.append(x)
    shuffle(s)


# to start game
# deal 1 up card to player and 1 down card to dealer
# deal second up card to player and up card to dealer
def deal_start(deck):
    for x in range(1, 5):
        if x % 2 == 0:
            player["cards"].append(deck.pop(0))
        else:
            dealer["cards"].append(deck.pop(0))


def deal_card(deck):
    return deck.pop(0)


# this should handle all possible combinations
def get_hand_values(hand):
    hand_value = 0
    ace_count = 0

    for x in hand:
        hand_value += values[x]
        if x == "A":
            ace_count += 1

    while ace_count > 0 and hand_value > 21:
        hand_value -= 10
        ace_count -= 1

    return hand_value


def update_hand_value(player, dealer):
    player["total"] = get_hand_values(player["cards"])
    dealer["total"] = get_hand_values(dealer["cards"])


def check_blackjack(hand):
    face_cards = ["10", "J", "Q", "K"]

    if len(hand) == 2:
      if hand[0] == "A" or hand[1] == "A":
        if hand[0] in face_cards or hand[1] in face_cards:
          return True

    return False


def show_cards(player, dealer):
    if player["stand"] == False:
      tmp = dealer["cards"][0]
      dealer["cards"][0] = "?"
      print("\nDealer: " + " - ".join(dealer["cards"]))
      print("Dealer Total: ", dealer["total"] - values[tmp])
      dealer["cards"][0] = tmp
    else:
      print("Dealer: " + " - ".join(dealer["cards"]))
      print("Dealer Total: ", dealer["total"])

    print("\nPlayer: " + " - ".join(player["cards"]))
    print("Player total: ", player["total"])


# this could probably be cleaner
def check_win(player, dealer):
    if player["total"] > 21:
        print("\nBust ! Dealer Wins")
        return
    elif dealer["total"] > 21 and player["total"] <= 21:
        print("\nDealer Busts ! You Win !")
    elif (player["total"] == dealer["total"]) and (player["total"] <= 21 and dealer["total"] <= 21):
        print("\nPush !")
        return
    elif player["total"] < 21 and dealer["total"] > 21:
        print("\nYou Win !")
        return
    elif player["total"] > dealer["total"] and player["total"] <= 21:
        print("\nYou Win !")
        return
    else:
        print("\nDealer Wins !")


def action_menu():
  print("\nActions:")
  print("1: hit")
  print("2: stand\n")


def get_action():
  choice = 0

  while True:
    try:
      choice = int(input("hit or stand: "))
      if choice == 1 or choice == 2:
        break
      else:
        print("invalid action...")
    except ValueError:
      print("invalid action...")

  return choice


# main game loop
def game():
    build_shoe(shoe)
    deal_start(shoe)
    update_hand_value(player, dealer)


    if check_blackjack(player["cards"]) or check_blackjack(dealer["cards"]):
      player["stand"] = True
      print("BlackJack !")

    show_cards(player, dealer)


    while player["stand"] == False:
      action_menu()
      action = get_action()

      if action == 1:
        player["cards"].append(deal_card(shoe))
        update_hand_value(player, dealer)
        show_cards(player, dealer)
        if player["total"] > 21:
          player["stand"] = True
      elif action == 2:
        player["stand"] = True


    while dealer["total"] < 17:
      dealer["cards"].append(deal_card(shoe))
      update_hand_value(player, dealer)

    show_cards(player, dealer)

    check_win(player, dealer)


game()
