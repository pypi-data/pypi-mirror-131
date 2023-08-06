#!/usr/bin/env python
import webbrowser
from termcolor import colored
import sys as sys

from .error import SearchError
from .utility import Utility
from .utility import Playbook
from .save import SaveSearchResults
from .update import UpdateApplication
from .api_test import ApiTesting
from .notion import NotionClient

version = "0.1.0"


class Prompt:
    def __init__(self, message):
        self.message = message

    def prompt(self):
        print(colored(f"{self.message} : ", "cyan"), end="")
        data = input()
        return data


class Search:
    def __init__(self, arguments):
        self.arguments = arguments
        self.utility_object = Utility()
        self.api_test_object = ApiTesting()
        self.playbook_object = Playbook()

    def search_args(self):
        if self.arguments.search:
            self.search_for_results()
        elif self.arguments.file:
            self.search_for_results(True)
        elif self.arguments.playbook:
            self.playbook_object.display_panel()
        elif self.arguments.new:
            url = "https://stackoverflow.com/questions/ask"
            if isinstance(self.arguments.new, str):
                webbrowser.open(f"{url}?title={self.arguments.new}")
            else:
                webbrowser.open(url)
        elif self.arguments.custom:
            self.utility_object.setCustomKey()
        elif self.arguments.update:
            update = UpdateApplication(version)
            update.check_for_updates()
        elif self.arguments.GET:
            self.api_test_object.get_request()
        elif self.arguments.POST:
            self.api_test_object.post_request()
        elif self.arguments.DELETE:
            self.api_test_object.delete_request()
        elif self.arguments.notion:
            NotionClient().get_tokenv2_cookie()

    def search_for_results(self, save=False):
        queries = ["What do you want to search", "Tags"]
        query_solutions = []

        # ask question
        for each_query in queries:
            # Be careful if there are
            # KeyBoard Interrupts or EOErrors
            try:
                prompt = Prompt(str(each_query)).prompt()
                if each_query == "Tags":
                    continue
                if prompt.strip() == "":
                    SearchError(
                        "\U0001F613 Input data empty", "\U0001F504 Please try again "
                    )
                    sys.exit()
            except:
                sys.exit()

            query_solutions.append(prompt)

        question, tags = (
            query_solutions[0],
            query_solutions[1] if len(query_solutions) > 1 else "",
        )
        json_output = self.utility_object.make_request(question, tags)
        questions = self.utility_object.get_que(json_output)
        if questions == []:
            # evoke an error
            SearchError("\U0001F613 No answer found", "\U0001F604 Please try reddit")
        else:
            data = self.utility_object.get_ans(questions)
            print(
                """
            \U0001F604  Hopefully you found what you were looking for!
            \U0001F4C2  You can save an answer to a file with '-file'

            Not found what you were looking for \U00002754
            \U0001F4C4  Open browser and post your question
                on StackOverflow with '-n [title (optional)]'

            \U0001F50E  To search more use '-s'
            """
            )

            if save:
                filename = SaveSearchResults(data)
                print(
                    colored(
                        f"\U0001F604 Answers successfully saved into {filename}",
                        "green",
                    ),
                    colored(
                        "\U0001F604 Answers successfully saved into" + filename, "green"
                    ),
                )
