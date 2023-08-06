user_input = input("Enter items names: ")
user_input = user_input.split(',')
my_dictionary={"black padded Trench Coat":150, "Camel oversized coat":90, "Grey Trench Coat":200, "Ripped Denim Jacket":180, "Oliver Bomber Jacket":80,"Black zipper Check Bomber Jacket":100,"Sequin Jacket":150,"Sparkle Denim Jacket":130,"Grey Hoodie":90,"Grey Overalls":150}
total_price = 0

for items in user_input:
    try:
        total_price = total_price + my_dictionary[items]
    except:
        total_price = "Some groceries are not avaiable in the dictionary."
        break

print(total_price)
