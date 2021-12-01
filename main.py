def processCmd(ans):
  if ans == "/exit":
    return 0
  elif ans == "/help":
    print("help!")
  else:
    print(ans, "-- not a valid command. Type /help to see a list of commands.")

def main():
  print("Welcome to BullyPy!")
  print("-------------------")
  print("Enter /help to see list of available commands")

  while True:
    cmd = processCmd(input("$ "))
    if cmd == 0:
      return 0

main()
