import subprocess

def runCmd(cmd):
    proc = subprocess.Popen([cmd + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()

    return (out.decode("utf-8").strip(), err.decode("utf-8").strip())

def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()