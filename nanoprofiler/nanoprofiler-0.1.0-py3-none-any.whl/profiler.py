import cProfile, pstats, io, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd

fontP = FontProperties()
fontP.set_size('small')

def remove_empty(l):
    """Removes all empty strings from a list

    Args:
        l (list): List containing strings

    Returns:
        list: List with empty strings removed
    """
    while "" in l: l.remove("")
    return l

def to_float(n):
    try:
        return float(n)
    except:
        return n

class Profiler:
    def __init__(self, dfs={}):
        self.dfs = dfs
        self.gotData = len(dfs) > 0
        self.count = len(dfs)
        self.name = ""

    def set_cprofiler(self, name=""):
        """Instances a cProfile to use inside code, user should use enable and disable methods 
        of cProfile object to control the profiler, after the execution finished call stop to
        store results.

        Args:
            name (str, optional): Name of the execution, if none will be stored the count of 
                executions. Defaults to "".

        Returns:
            cProfile: cProfile object
        """
        # If no execution name given generates one based on the count of executions
        if name == "":
            name = "exec {:}".format(self.count)
        # Stores name and instances and return cProfile
        self.name = name
        self.profiler = cProfile.Profile()
        return self.profiler

    def start(self, name=""):
        """Instances and enables a cProfile object to start profiling immediately 

        Args:
            name (str, optional):  Name of the execution, if none will be stored the count of 
                executions. Defaults to "".
        """
        # If no execution name given generates one based on the count of executions
        if name == "":
            name = "exec {:}".format(self.count)
        # Stores name and enables cProfile
        self.name = name
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def stop(self):
        """Disables cProfile object, parse and stores results of current execution

        Raises:
            RuntimeWarning: User should not call stop without calling start() or set_cprofiler() 
        """
        if self.name == "":
            raise RuntimeWarning('Must call start() before stop()!')
        else:
            # Disables cProfile and stores results in a string
            self.profiler.disable()
            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(self.profiler, stream=s).sort_stats(sortby)
            ps.print_stats()
            # Get results headers
            results = remove_empty(s.getvalue().split('\n')[4:])
            headers = remove_empty(results[0].split(" "))
            headers[2] = headers[2]+"_"+headers[1]
            headers[4] = headers[4]+"_"+headers[3]
            headers[5] = 'function'
            # Parse data
            results = results[1:]
            data = {}
            for header in headers:
                data[header] = []
            for result in results:
                # Split every line with spaces and remove empty strings from resulting list
                line = remove_empty(result.split(" "))
                # Stores respective columns in data
                for i in range(len(headers)):
                    data[headers[i]].append(to_float(line[i]))
                # If line is bigger than headers, function name has spaces, append all excess items to function name
                if len(line) > len(headers):
                    for i in range(len(headers), len(line)):
                        data[headers[-1]][-1] = data[headers[-1]][-1] + " " + line[i]
            # Add extra keys to treat function name
            data['filename'] = []
            data['direc'] = []
            data['line'] = []
            data['short_name'] = []
            for i in range(len(data['function'])):
                # Standard function name: filename:lineno(function)
                if ":" in data['function'][i] and "(" in data['function'][i] and ")"  in data['function'][i]:
                    filename = data['function'][i][:-1].split(":")[0]
                    if "\\" in filename or "/" in filename:
                        direc, filename = os.path.split(filename)
                    else:
                        direc = ""
                    line = data['function'][i][:-1].split(":")[-1].split("(")[0]
                    function = data['function'][i][:-1].split(":")[-1].split("(")[1]
                    name = function+":"+line+"("+filename+")"
                # Method of imported objects: {method 'name' of 'class' objects}
                elif "{method" in data['function'][i]:
                    function = data['function'][i][:-1].split("'")[1]
                    filename = data['function'][i][:-1].split("'")[3]
                    name = function+"("+filename+")"
                    direc = ""
                    line = ""
                # Method of built-in objects: {built-in method class.method}
                elif "{built-in method" in data['function'][i]:
                    function = data['function'][i][:-1].split(" ")[2].split(".")[-1]
                    filename = data['function'][i][:-1].split(" ")[2].split(".")[:-1]
                    name = data['function'][i][:-1].split(" ")[2]
                    direc = ""
                    line = ""
                # If no match to any above just copy it
                else:
                    function = data['function'][i]
                    name = data['function'][i]
                    filename = ""
                    direc = ""
                    line = ""
                # Store parsed names to data
                data['function'][i] = function
                data['filename'].append(filename)
                data['direc'].append(direc)
                data['line'].append(line)
                data['short_name'].append(name)
            # Creates a dataFrame with data and append to dfs list
            df = pd.DataFrame.from_dict(data)
            self.dfs[self.name] = (df)
            self.gotData = True
            self.count += 1
            self.name = ""
            del self.profiler

    def list_results_keys(self):
        if self.gotData:
            return self.dfs.keys()
        else:
            raise RuntimeWarning('Called results before disable')

    def results(self):
        if self.gotData:
            return self.dfs
        else:
            raise RuntimeWarning('Called results before disable')

    def load_results(self, direc, name):
        """Load results from files.

        Args:
            direc (string): Directory where results where stored.
            name (string): Prefix name for the files.
        """
        try:
            all_files = list(os.walk(direc))[0][2]
        except:
            print("Could not find files in the specified directory.")
            return None
        csv_files = []
        for f in all_files:
            if f[-4:] == ".csv" and f[:len(name)] == name:
                filename = os.path.join(direc, f)
                key = f[len(name)+1:-4]
                csv_files.append((key, filename))
        csv_files.sort(key=lambda x: int(x[0]))
        for key, f in csv_files:
            try:
                df = pd.read_csv(f)
                self.dfs[key] = df
                self.gotData = True
            except:
                pass

    def plot_top_time(self, filename=False, time="cumtime", keys=[], title="", n=10, size=(5, 4)):
        """Plots a bar plot for all given keys with the top n functions.

        Args:
            filename (bool, optional): File to store plot. Defaults to False.
            time (str, optional): Cumulative time ("cumtime") or total time ("tottime") to plot. Defaults to "cumtime".
            keys (list, optional): List of execution keys to be ploted, if none is passed will plot all keys.
            title (bool, optional): Plot title. Defaults to False.
            n (int, optional): Number of functions to plot if not given list of functions. Defaults to 10.
            size (tuple, optional): Size of the plot, tuple of floats in inches. Defaults to (5, 4).

        Raises:
            RuntimeWarning: User tried to plot without data.
        """
        if self.gotData:
            if keys == []:
                keys = self.list_results_keys()
            for key in keys:
                df = self.dfs[key].sort_values(time, ascending=False)
                plt.figure(figsize=size)
                plt.bar(df.iloc[:n].function, df[time].iloc[:n], label=key)
                ax = plt.gca()
                ax.set_xlabel("Function")
                if time == "cumtime":
                    ax.set_ylabel("Cumulative time (s)")
                elif time == "tottime":
                    ax.set_ylabel("Total time (s)")
                else:
                    ax.set_ylabel("time (s)")
                plt.title(title+key+" ("+time+")")
                plt.legend(loc='upper right')
                plt.xticks(rotation=45, horizontalalignment='right')
                if filename:
                    plt.savefig(filename+"_"+time+"_"+key+".pdf")
        else:
            raise RuntimeWarning('Called results before disable')

    def plot_function(self, functions=[], n=10, filename=False, time="cumtime", percent=False, title=False, log_scale=False, legend_outside=False, xlabel="Execution label", size=(5, 4)):
        """Plot the time in each function, by default plots the cumulative time for the top 10 functions 

        Args:
            functions (list, optional): Functions to plot, if none given will plot top n functions.
            n (int, optional): Number of functions to plot if not given list of functions. Defaults to 10.
            filename (bool, optional): File to store plot. Defaults to False.
            time (str, optional): Cumulative time ("cumtime") or total time ("tottime") to plot. Defaults to "cumtime".
            percent (bool, optional): Plot values as percent instead of seconds. Defaults to False.
            title (bool, optional): Plot title. Defaults to False.
            log_scale (bool, optional): Log in the y axis. Defaults to False.
            legend_outside (bool, optional): Puts the legend ouside the plot. Defaults to False.
            xlabel (str, optional): Label for the x axis. Defaults to "Execution label".
            size (tuple, optional): Size of the plot, tuple of floats in inches. Defaults to (5, 4).

        Raises:
            RuntimeWarning: User tried to plot without data.
        """
        if self.gotData:
            keys = list(self.dfs.keys())
            # if not passed as parameters get the top n functions from the last execution
            if functions == []:
                df = self.dfs[keys[-1]].sort_values(time, ascending=False)
                functions = df.iloc[:n].function.tolist()
            # Initialize empty arrays to store results
            y = np.zeros((len(self.dfs), len(functions)), dtype=float)
            x = np.arange(len(self.dfs))
            # Iterate on all executions
            for i in range(len(self.dfs)):
                # Load the dataframe sorting by the column defined by time
                df = self.dfs[keys[i]].sort_values(time, ascending=False)
                exectime = np.sum(df['tottime'])
                # Iterate on all functions
                for j in range(len(functions)):
                    # Try to load results with exact match to function name
                    lines = df.loc[df.function == functions[j]]
                    # If unable to select a line by exact match try the first line that contais the function name
                    if lines.function.count() == 0:
                        lines = df.loc[df.function.str.contains(functions[j])]
                    # If successful in selecting a line
                    if lines.function.count() >= 1:
                        # Stores the value in y
                        y[i, j] = lines[time].iloc[0]
                        # If the plot is percent divides by the execution time
                        if percent:
                            y[i, j] = y[i, j]*100./exectime
                        # Saves the exact name of the function loaded
                        if i == (len(self.dfs)-1):
                            functions[j] = lines.iloc[0].function

            # Start plot
            plt.figure(figsize=size)
            # If got title as parameter print it
            if title:
                plt.title(title)
            # Generates y label
            if time == "cumtime":
                yLabel = "Cumulative time"
            elif time == "tottime":
                yLabel = "Total time"
            else:
                yLabel = time + " time"
            if percent:
                yLabel = yLabel + " (%)"
            else:
                yLabel = yLabel + " (s)"
            # Print labels and plot
            ax = plt.gca()
            ax.set_xlabel(xlabel)
            ax.set_ylabel(yLabel)
            plt.plot(x, y)
            # Print legend according to parameters
            if legend_outside:
                plt.legend(functions, loc='center left', bbox_to_anchor=(1, 0.5))
            else:
                plt.legend(functions)
            if log_scale:
                plt.yscale("log")
            plt.xticks(x, keys)
            plt.tight_layout(pad=0.5)
            # Given fimename saves pdf
            if filename:
                plt.savefig(filename)
        else:
            raise RuntimeWarning('Called results before disable')

    def save_data(self, out):
        """Saves data in csv files.

        Args:
            out (string): Filename to save files, "_name.csv" will be appended for each execution
        """
        for key in self.dfs.keys():
            self.dfs[key].to_csv(out+"_{:}.csv".format(key))