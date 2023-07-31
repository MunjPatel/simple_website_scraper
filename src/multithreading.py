import requests as re
from bs4 import BeautifulSoup
from fuzzywuzzy.fuzz import token_set_ratio
from src.utils import log_instance, FakeUserAgent
from scraper_exceptions.exceptions import ZeroResultsError, ZeroUrlError, WaitTimeError
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError, HTTPError, ConnectTimeout, Timeout

ua_instance = FakeUserAgent()
user_agent = ua_instance.fake_ua()

class SimilarityScore:
    """
    
    Method that generates dictionary of url and similarity %.

    Inputs: self
    Outputs: list
        
    """
    def calculate(self,url:str,input_string:str, wait_time:int)->dict:
        try:
            response = re.get(url,timeout=wait_time, headers={'User-Agent':user_agent})
            if response.status_code == 200:
                text = BeautifulSoup(response.text, "html.parser")
                for data in text("style", "script"):
                    data.decompose()
                text = " ".join(text.stripped_strings).encode("ascii", "ignore").decode()
                score = token_set_ratio(text, input_string)
                log_instance.get_info(f"{url} responded successfully. Similarity = {score}%.")
                return {url:score}
            else:
                log_instance.get_warning(f"{url} failed to respond, skipping it.")
                return {url:0}
        except ConnectionError:
                log_instance.get_critical(str(ConnectionError(f"Encountered an error while trying to connect to {url}")))
        except HTTPError:
                log_instance.get_critical(str(HTTPError(f"Request to {url} unsuccessfull.")))
        except ValueError:
                log_instance.get_critical(str(ValueError(f"Failed to decode server json response from {url}.")))
        except ConnectTimeout:
                log_instance.get_critical(str(ConnectTimeout(f"Request timed-out while trying to connect to {url}.")))
        except Timeout:
                log_instance.get_critical(str(Timeout(f"{url} failed to complete request in timeout-period.")))
        except Exception as e:
                log_instance.get_critical(str(Exception(f"Following error occured: {str(e)} when trying to connect to {url}")))



class MultipleRequests:
    def __init__(self)->None:
        pass
    def parallel_requests(self,urls:list,input_string:str, wait_time:int)->dict:
        if type(urls) == list and len(urls) > 0 and type(input_string) == str and type(wait_time) == int and wait_time > 0:
            log_instance.clear_logs()
            log_instance.get_critical(arg=":::Checking for responsive links:::")
            executor = ThreadPoolExecutor(max_workers=int((len(urls)/2)*1.75))
            futures = [executor.submit(SimilarityScore().calculate,link, input_string, wait_time) for link in urls]
            results = [future.result() for future in futures]
            results = [result for result in results if type(result) == dict]
            result_zero = [result for result in results if list(result.values())[0] == 0]
            log_instance.get_critical(f"Zero similarity urls removed count = {len(result_zero)}.")
            modified_results = {list(result.keys())[0]:list(result.values())[0] for result in results if list(result.values())[0] != 0}
            modified_results = dict(sorted(modified_results.items(), key=lambda item: item[1], reverse=True))
            log_instance.get_info(f"Output generated:")
            log_instance.get_critical(f"Number of unique keys formed = {len(modified_results)}.")
            if len(modified_results) != 0:
                return modified_results
            else:
                raise ZeroResultsError(f"Number of unique keys format: {len(modified_results)}. Make sure you have stable internet connection.")
        elif len(urls) == 0:
             raise ZeroUrlError(f"Expected 'urls' to be a non-empty list.")
        elif type(urls) != list:
            raise TypeError(f"Expected 'urls' argument of type {list}, got {type(urls)} instead.")
        elif type(input_string) != str:
            raise TypeError(f"Expected 'input_string' argument of type {str}, got {type(input_string)} instead.")
        elif type(wait_time) != int:
            raise TypeError(f"Expected 'wait_time' argument of type {int}, got {type(wait_time)} instead.")
        elif wait_time <= 0:
            raise WaitTimeError(f"Expected 'wait_time' argument to be a non-zero positive integer, given {wait_time} instead.")


if __name__ == "__main__":
    urls = ['https://www.pythonpool.com/python-setuptools/', 'https://www.blog.pythonlibrary.org/2021/09/23/python-101-how-to-create-a-python-package/', 'https://slash64.tech/including-non-python-files-with-a-python-project/', 'https://www.gnu.org/software/pyconfigure/manual/html_node/setup_002epy_002ein.html', 'https://simonwillison.net/2021/Nov/4/publish-open-source-python-library/', 'https://www.oak-tree.tech/blog/python-packaging-primer','https://naucse.python.cz/2020/tieto-ostrava-jaro/beginners/tieto-packaging/', 'https://babel.pocoo.org/en/latest/setup.html', 'https://readthedocs.web.cern.ch/plugins/servlet/mobile', 'https://thepythonguru.com/writing-packages-in-python/', 'https://cets.seas.upenn.edu/answers/install-python-module.html', 'https://lightrun.com/answers/davhau-mach-nix-problems-with-installing-package-that-doesnt-use-setuppy', 'https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/', 'https://ianhopkinson.org.uk/2022/02/understanding-setup-py-setup-cfg-and-pyproject-toml-in-python/', 'https://www.mssqltips.com/sqlservertip/6802/create-wheel-file-python-package-distribute-custom-code/', 'https://www.pythonforthelab.com/blog/how-create-setup-file-your-project/', 'https://www.jetbrains.com/help/pycharm/creating-and-running-setup-py.html', 'https://www.osc.edu/book/export/html/3004', 'https://medium.datadriveninvestor.com/how-to-create-a-python-package-for-django-and-publish-it-in-pypi-76152e587691', 'https://docs.python.org/3/distutils/setupscript.html', 'https://towardsdatascience.com/setuptools-python-571e7d5500f2', 'https://www.pythoncheatsheet.org/cheatsheet/setup-py', 'https://write.agrevolution.in/packaging-a-django-project-using-setuptools-c1d7d565779e', 'https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/', 'https://amir.rachum.com/python-entry-points/', 'https://www.turing.com/kb/7-ways-to-include-non-python-files-into-python-package', 'https://www.ibm.com/docs/SSCH7P_3.8.0/distutils.html', 'https://martin-thoma.com/python-package-versions/', 'https://www.linode.com/docs/guides/installing-and-importing-modules-in-python-3/', 'https://datacarpentry.org/semester-biology/materials/packaging/', 'https://lappweb.in2p3.fr/~paubert/ASTERICS_HPC/6-7-4-1416.html', 'https://docs.python-guide.org/writing/structure/', 'https://queirozf.com/entries/package-a-python-project-and-make-it-available-via-pip-install-simple-example', 'https://www.infoworld.com/article/3656628/6-ways-to-package-python-apps-for-re-use.html', 'https://www.tutorialsteacher.com/python/python-package', 'https://docs.snyk.io/snyk-cli/test-for-vulnerabilities/why-is-my-setup.py-file-failing-to-scan-or-finding-0-dependencies', 'https://github.com/microsoft/LightGBM/issues/5061', 'https://www.tutorialspoint.com/How-to-install-a-Python-Module', 'https://stackoverflow.com/questions/64435188/setup-py-install-vs-pip-install', 'https://medium.com/', 'https://www.geeksforgeeks.org/what-is-setup-py-in-python/', 'https://pypi.org/project/setup-py-cli/', 'https://stackoverflow.com/questions/43658870/requirements-txt-vs-setup-py', 'https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications', 'https://christophergs.com/python/2016/12/11/python-setuptools/', 'https://click.palletsprojects.com/en/8.1.x/setuptools/', 'https://www.kdnuggets.com/2018/06/packaging-distributing-python-project-pypi-pip.html/2', 'https://www.w3docs.com/snippets/python/what-is-setup-py.html', 'https://www.devdungeon.com/content/python-packaging-tutorial', 'https://doc.dataiku.com/dss/latest/python/packages.html', 'https://flynn.gg/blog/creating-a-python-package/', 'https://blog.gitnux.com/code/python-setup-py/', 'https://kb.iu.edu/d/acey', 'https://www.redhat.com/sysadmin/packaging-applications-python', 'https://lincolnloop.com/insights/using-setuppy-your-django-project/', 'https://www.quora.com/What-is-the-Python-setup-py-file-for', 'https://pythonhosted.org/an_example_pypi_project/setuptools.html', 'https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/', 'https://betterprogramming.pub/sharing-code-using-a-setup-py-b6a596646532', 'https://drivendata.co/blog/python-packaging-2023', 'https://www.reddit.com/r/learnpython/comments/5egqfo/what_is_the_difference_between_init_py_and_setuppy/', 'https://code.visualstudio.com/docs/python/python-tutorial', 'https://diveintopython3.net/packaging.html', 'https://wiki.archlinux.org/title/Python_package_guidelines', 'https://docs.python.org/3/distutils/sourcedist.html', 'https://docs.gammapy.org/0.6/install/pip.html', 'https://pgjones.dev/blog/packaging-without-setup-py-2020/', 'https://docs.aws.amazon.com/lambda/latest/dg/python-package.html', 'https://opensource.com/article/23/1/packaging-python-modules-wheels', 'https://docs.python.org/3/distutils/configfile.html', 'https://levelup.gitconnected.com/requirements-txt-vs-setup-py-in-python-a0e70313f50b', 'https://stackoverflow.com/questions/12324601/how-to-install-a-python-module-via-its-setup-py-in-windows', 'https://stackoverflow.com/questions/1471994/what-is-setup-py', 'https://roboticsbackend.com/ros-import-python-module-from-another-package/', 'https://www.linkedin.com/pulse/create-python-package-share-pip-install-your-team-anirban-hati', 'https://www.depts.ttu.edu/hpcc/userguides/application_guides/python.packages.local_installation.php', 'https://changhsinlee.com/python-package/', 'https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html', 'https://www.pantsbuild.org/v1.29/docs/python-setup-py-goal', 'https://packaging-guide.openastronomy.org/en/latest/minimal.html', 'https://docs.python.org/3/distutils/introduction.html', 'https://dev.to/bowmanjd/python-dev-environment-part-1-setup-py-venv-and-pip-22gd', 'https://www.educative.io/answers/what-is-setuppy', 'https://www.py2exe.org/index.cgi/Tutorial', 'https://itnext.io/python-packaging-12ef040c4ea0', 'https://stackabuse.com/creating-executable-files-from-python-scripts-with-py2exe/', 'https://superuser.com/questions/609116/how-to-include-python-modules-not-under-distribution-root-in-setup-py', 'https://pybit.es/articles/how-to-package-and-deploy-cli-apps/', 'https://pythonpackaging.info/02-Package-Structure.html', 'https://copdips.com/2022/09/adding-data-files-to-python-package-with-setup-py.html', 'https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/', 'https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html', 'https://setuptools.pypa.io/en/latest/userguide/quickstart.html', 'https://www.activestate.com/resources/quick-reads/how-to-manually-install-python-packages/', 'https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/', 'https://realpython.com/pypi-publish-python-package/', 'https://www.delftstack.com/howto/python/python-setup.py/', 'https://holypython.com/python-packaging-local-installation-tests-before-uploading/', 'https://timothybramlett.com/How_to_create_a_Python_Package_with___init__py.html', 'https://stackoverflow.com/questions/60145069/what-is-the-purpose-of-setup-py']
    query = "Setup tools in python."
    # scores = {}
    # for link in urls:
    #     query = "Setup tools in python."
    #     scores[link] = SimilarityScore().calculate(link,query,wait_time=10)
    # print(scores)
    instance = MultipleRequests()
    results = instance.parallel_requests(urls=urls, input_string=query, wait_time=10)
    print(results)