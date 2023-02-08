import sys

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#print(sys.argv[0])

def main(arg1,arg2):
    print(arg1)
    print(arg2)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])