
def score(delivery):
    s = 0
    for _, team in delivery:
        ingredients = set()
        for pizza in team:
            ingredients.update(pizza_ingredients[pizza])
        s += len(ingredients) ** 2
    return s


def delivery(team_size):
    potential_delivery = []
    current_ingredients = set()
    # select pizza for each team member
    for _ in range(team_size):

        # mark which pizza to add
        pizza_to_add = -1
        min_overlap = 0
        max_ingredients_added = 0
        for pizza in undelivered:

            # pizza already added
            if pizza in potential_delivery:
                continue

            # early pruning if max already achieved
            if len(pizza_ingredients[pizza]) < max_ingredients_added:
                break

            # check list of ingredients if new pizza is added
            overlapped_ingredients = current_ingredients & set(
                pizza_ingredients[pizza])

            overlap_size = len(overlapped_ingredients)
            ingredients_added = len(pizza_ingredients[pizza]) - overlap_size

            # if more ingredients will be added, or no improvement but least overlap
            if (ingredients_added > max_ingredients_added) or (overlap_size < min_overlap):
                pizza_to_add = pizza
                min_overlap = overlap_size
                max_ingredients_added = ingredients_added
                # cannot find a smaller overlap
                if min_overlap == 0:
                    break

        # if a suitable pizza is found, add it to the potential delivery
        if pizza_to_add > -1:
            potential_delivery.append(pizza_to_add)
            current_ingredients = current_ingredients | set(
                pizza_ingredients[pizza_to_add])

        # cannot add new pizza that will increase the score, stop
        else:
            break

    for pizza in potential_delivery:
        undelivered.remove(pizza)

    return potential_delivery


inputs = ['a_example', 'b_little_bit_of_everything.in',
          'c_many_ingredients.in', 'd_many_pizzas.in', 'e_many_teams.in']
for input in inputs:
    f = open(input, 'r').read().splitlines()
    t = [0] * 5
    (pizza_num, t[2], t[3], t[4]) = [int(i) for i in f[0].split(' ')]

    pizza_ingredients = [pizza.split(' ')[1:] for pizza in f[1:]]
    pizzas_indexes = [i for i in range(pizza_num)]

    undelivered = [i for _, i in sorted(
        zip(pizza_ingredients, pizzas_indexes), key=lambda pair: len(pair[0]), reverse=True)]

    deliveries = []

    while (len(undelivered) >= 2):
        max_delivery = 0
        for i in range(4, 1, -1):
            if t[i] > 0:
                max_delivery = i
                break
        if max_delivery == 0:
            break

        # try to create a delivery
        potential_delivery = delivery(max_delivery)

        # delivery smaller than max
        if t[len(potential_delivery)] == 0:
            # Increase delivery size with the pizzas with the least ingredients
            while (len(undelivered) > 0):
                potential_delivery.append(undelivered.pop(-1))
                if t[len(potential_delivery)] > 0:
                    break
        deliveries.append((len(potential_delivery), potential_delivery))
        t[len(potential_delivery)] -= 1
    print(score(deliveries))
