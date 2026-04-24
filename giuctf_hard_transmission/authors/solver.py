# pip install py-enigma

from enigma.machine import EnigmaMachine

ciphertext = "PSKHQOWDFIUERWRNJZLVCSZOKNRWDDLFAXOQTTLAUVSGNYK"

machine = EnigmaMachine.from_key_sheet(
    rotors="VII II V",
    reflector="B",
    ring_settings="A A A",
    plugboard_settings="BQ CR DI EJ KW MT OS PX UZ GH"
)

machine.set_display("AQL")

plaintext = machine.process_text(ciphertext.upper())
print(plaintext)