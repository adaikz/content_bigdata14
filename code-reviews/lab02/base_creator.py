#!/opt/anaconda/envs/bd9/bin/python3
import happybase


def main():
    connection = happybase.Connection('bd-master.newprolab.com')
    try:
        connection.delete_table("sergey.korolev", disable=True)
    except:
        pass

    urls = {
        'UID': dict(),
        'URL': dict()
    }

    connection.create_table("sergey.korolev", urls)


if __name__ == "__main__":
    main()
