import pandas
import os
import plotly.graph_objs as graph_objects
from plotly.graph_objs import Layout
from plotly.offline import iplot, offline
import plotly
import ipywidgets as widgets

from datetime import datetime, timedelta

class ForgePlot:
    def __init__(self):
        self.standard_button = widgets.Button(
            description='Standard Plot',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Create a Standard Forge Nano Plot',
        )
        self.standard_button.on_click(self.go_standard)

        self.overlay_button = widgets.Button(
            description='Overlay Plot',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Create an Overlay Forge Nano Plot',
        )

        self.kwikplot_button = widgets.Button(
            description='Kwik Plot',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Create a Kwiky',
        )

        self.min_flu_button = widgets.Button(
            description='Min Flu Plot',
            disabled=False,
            button_style='info',
            tooltip='Minimum Fluidization Plot',
        )

        self.standard_button.on_click(self.go_standard)
        self.overlay_button.on_click(self.go_overlay)
        self.kwikplot_button.on_click(self.go_kwikplot)
        self.min_flu_button.on_click(self.go_minflu)

        self.choice_label = widgets.Label('Choose Your Adventure....')

        self.button_box = widgets.HBox(children=[self.standard_button, self.overlay_button, self.kwikplot_button, self.min_flu_button])

        self.choice_box = widgets.VBox(children=[self.choice_label, self.button_box])
        display(self.choice_box)

    def go_standard(self, sender):
        self.choice_box.close()
        sp = StandardPlot()

    def go_overlay(self, sender):
        self.choice_box.close()
        op = OverlayPlot()

    def go_kwikplot(self, sender):
        self.choice_box.close()
        kp = KwikPlot()

    def go_minflu(self, sender):
        self.choice_box.close()
        mf = MinFluPlot()

#==============================================================================
#==================================== MIN FLU =================================
class MinFluPlot():
    def __init__(self):
        plotly.offline.init_notebook_mode(connected=True)
        # # self.do_y2_axis = False
        # self.go_button_visible = False
        # self.go_button = None
        self.main_chart= None
        self.trace_list = []
        self.x_axis_title = "DP"
        self.y_axis_title = "Flow Rate"
        # self.y_axis2_title = "Not Set"
        self.chart_title = "Min Flu Plot"
        # self.y_axis_options = {}
        # self.chart_width = 800
        # self.chart_height = 400
        # self.full_data = None
        # self.time_range = dict
        # self.lower_time_limit = '2017-11-07 17:00:00'
        # self.upper_time_limit = '2017-11-07 18:00:00'
        # self.plot_range_data = None
        # self.chart_built = False
        self.layout = None
        self.reg_col_list = []
        self.status_label = widgets.Label()
        

        #======================================= FILE MANAGER WIDGETS
        self._file_manager_box = widgets.VBox()
        self.file_manager_box = widgets.HBox()
        self.file_list_box = widgets.VBox()
        self.choice_label = widgets.Label('Min Flu Plot: 1 File Expected')
        self.check_for_files_button = widgets.Button(
            description='Check for Files',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Check for The Important ForgeNano Files',
            icon='check'
        )
        self.check_for_files_button.on_click(self.get_file_list)
        self.import_files_button = widgets.Button(
            description='Import File',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Import This Important File',
            icon='check'
        )
        self.import_files_button.on_click(self.import_files)
        self.get_file_list('sender')
        self.file_manager_box.children = [self.check_for_files_button, self.import_files_button, self.file_list_box]
        self._file_manager_box.children = [self.choice_label, self.file_manager_box]

        #Chart Title Widgets
        self.chart_title_entry = widgets.Text(self.chart_title)
        self.xaxis_title_entry = widgets.Text(self.x_axis_title)
        # self.yaxis_title_entry = widgets.Text(self.y_axis_title)
        # self.yaxis2_title_entry = widgets.Text(self.y_axis2_title)

        self.title_entry_box = widgets.VBox(children=[
            widgets.HBox(children=[widgets.Label('Chart Title:'), self.chart_title_entry]),
            # widgets.HBox(children=[widgets.Label('X Axis Title:'), self.xaxis_title_entry]),
            # widgets.HBox(children=[widgets.Label('Y Axis Title:'), self.yaxis_title_entry]),
            # widgets.HBox(children=[widgets.Label('Y Axis 2 Title:'), self.yaxis2_title_entry]),
        ])

        # self.chart_title_entry.observe(self.set_chart_title, names='value')
        # self.xaxis_title_entry.observe(self.set_xaxis_title, names='value')
        # self.yaxis_title_entry.observe(self.set_yaxis_title, names='value')
        # self.yaxis2_title_entry.observe(self.set_yaxis_title, names='value')

        #Options widgets
        self.flow_choice = widgets.Dropdown(options=self.reg_col_list,
                                            description='Flow Rate')

        self.exhaust_choice = widgets.Dropdown(options=self.reg_col_list,
                                                description='Exhaust PT')

        self.manifold_choice = widgets.Dropdown(options=self.reg_col_list,
                                                description='Manifold PT')

        self.max_flow_entry = widgets.Text('50')

        self.options_entry_box = widgets.VBox(children=[
            self.flow_choice, self.exhaust_choice, self.manifold_choice,
            widgets.HBox(children=[widgets.Label('Max Flow:'), self.max_flow_entry, widgets.Label('sccm')])
        ])

        self.main_accordian = widgets.Accordion(children=[
            self.title_entry_box, self.options_entry_box
        ])

        self.main_accordian.set_title(0, "Chart Titles")
        self.main_accordian.set_title(1, "Build Options")

        self.go_button = widgets.Button(
            description='Build Chart',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Build a Chart',
            icon='check'
        )

        self.go_button.on_click(self.build_chart)

        
        display(self.status_label)
        display(self._file_manager_box)

    def build_chart(self, sender):
        #Grab selected traces from the gui
        flow_rate_col = self.flow_choice.value
        exhaust_col = self.exhaust_choice.value
        manifold_col = self.manifold_choice.value
        
        #Create a temp file to write new values to
        temp_file = os.path.join(os.getcwd(), 'data/temp.csv')
        temp_file2 = os.path.join(os.getcwd(), 'data/temp2.csv')
        with open(temp_file, '+a') as _file:
            with open(temp_file2, '+a') as _file2:
                #write index name and column name in file
                _file.write("FLOW_RATE,DP\n")
                _file2.write("FLOW_RATE,DP\n")
                max_flow_reached = False
                #Iterate through imported data
                for i in range(0, len(self.full_data.index)-1):
                    #manifold - exhaust

                    #Get the values for this index item
                    flow = self.full_data[flow_rate_col][i]
                    manifold = self.full_data[manifold_col][i]
                    exhaust = self.full_data[exhaust_col][i]

                    #Calculate DP
                    dp = float(manifold) - float(exhaust)

                    if (not max_flow_reached) and (float(flow) >= float(self.max_flow_entry.value)):
                        max_flow_reached = True
                    elif (not max_flow_reached) and (float(flow) < float(self.max_flow_entry.value)):
                        _file.write("%s,%s\n" % (flow, dp))    
                        

                    if max_flow_reached and (float(flow) < float(self.max_flow_entry.value)):
                        _file2.write("%s,%s\n" % (flow, dp))
                        
                    

                    #Write new values to the files
                    # _file.write("%s,%s\n" % (flow, dp))

        #Import data from the new created file                
        new_data = pandas.read_csv(temp_file, index_col=0)    
        new_data2 = pandas.read_csv(temp_file2, index_col=0)  
        #Delete the new file
        os.remove(temp_file)
        os.remove(temp_file2)
        #Create the Trace
        self.trace_list.append(graph_objects.Scatter(
            x=new_data.index,
            y=new_data['DP'],
            name='DP Flow Increase',
            mode='markers',
        ))

        self.trace_list.append(graph_objects.Scatter(
            x=new_data2.index,
            y=new_data2['DP'],
            name='DP Flow Decrease',
            mode='markers',
            xaxis='x2',
            yaxis='y2'
        ))

        #Create the layout
        self.layout = Layout(title=self.chart_title_entry.value,
                             xaxis=dict(title='Flow Rate',
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20)),
                             yaxis=dict(title="DP",
                                        showgrid=True,
                                        linecolor='black',
                                        ticks='outside',
                                        anchor='x',
                                        domain=[0.6, 1]),
                            xaxis2=dict(title='Flow Rate',
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20),
                                        anchor='y2'
                                    ),
                             yaxis2=dict(title="DP",
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20),
                                        domain=[0, 0.4],
                                        anchor='x2'),
                             margin=dict(t=50),
                             autosize=False,
                             width=1300,
                             height=1600)

        #Create the chart
        self.main_chart = graph_objects.Figure(data=self.trace_list, layout=self.layout)
        self.status_label.value = 'Chart Built!'
        
        #Open the plot in a new window
        offline.plot(self.main_chart, filename="%s.html" % self.chart_title_entry.value)



    def get_file_list(self, sender):
        file_list = os.listdir('data')
        widget_list = []
        widget_list.append(widgets.Label('Files in Data Directory'))
        
        #We want only 1 file, so do some checking..
        if len(file_list) == 1:
            self.status_label.value = "Import A File!!"
            self.import_files_button.disabled = False
            for filename in file_list:
                widget_list.append(widgets.Label(filename))
        elif len(file_list) == 0:
            self.status_label.value = "No Files in Data Directory!"
            self.import_files_button.disabled = True
            widget_list.append(widgets.Label('No Files!'))
        elif len(file_list) > 1:
            self.import_files_button.disabled = True
            self.status_label.value = "Too Many Files in Data Directory!"
            for filename in file_list:
                widget_list.append(widgets.Label(filename))

        self.file_list_box.children = widget_list

    def import_files(self, sender):
        
        self.import_files_button.disabled = True
        filename_list = os.listdir('data')
        import_error = False
        error_message = "no error"
        # first = True
        self.status_label.value = 'Importing Files...'
        # display(self.status_label)
        for file_name in filename_list:
            self.status_label.value = 'Importing: %s' % file_name
            filename, extension = os.path.splitext(file_name)
            if extension == '.csv' or extension == '.CSV' or extension == '':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), index_col=0)
            elif extension == '.txt' or extension == '.TXT':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), delimiter='\t', index_col=0)
            else:
                # NO valid extensions found set data to None
                data = None

            if data is not None:
                try:
                    data.index = pandas.to_datetime(data.index)
                    self.full_data = data
                except ValueError as err:
                    import_error = True
                    error_message = err
            else:
                self.status_label.value = "Could not detect parsable file..."
                import_error = True
                error_message = "Could not detect parsable file!"

            
            # if first:
            #     first = False
                
            # else:
            #     self.full_data = self.full_data.join(data)
        # new_columns = []
        # for column in self.full_data.columns:
        #     new_col = column.strip()
        #     new_columns.append(new_col)
        # self.full_data.columns = new_columns
        # self.reg_col_list = []
        # for column in self.full_data:
        #          self.reg_col_list.append(column)

        # self.flow_choice.options = self.reg_col_list
        # self.exhaust_choice.options = self.reg_col_list
        # self.manifold_choice.options = self.reg_col_list
        # self.break_choice_entry.options = self.reg_col_list
        # self.trace_choice_entry.options = self.reg_col_list
        if import_error:
            self.status_label.value = 'Invalid Data File: %s \nPlease Try Again' % error_message
            self.check_for_files_button.disabled = True
            self.try_again = widgets.Button(
                description='Try Again...',
                disabled=False,
                button_style='danger',  # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Try Again...',
                icon='trash'
            )
            self.try_again.on_click(self.try_import_again)
            display(self.try_again)
        else:
            #Format columns for use
            new_columns = []
            for column in self.full_data.columns:
                new_col = column.strip()
                new_columns.append(new_col)
            self.full_data.columns = new_columns
            self.reg_col_list = []
            for column in self.full_data:
                    self.reg_col_list.append(column)

            self.flow_choice.options = self.reg_col_list
            self.exhaust_choice.options = self.reg_col_list
            self.manifold_choice.options = self.reg_col_list
            self._file_manager_box.close()
            self.status_label.value = 'Import Complete!'
            display(self.main_accordian)
            display(self.go_button)

    def try_import_again(self, sender):
        self.try_again.close()
        self.check_for_files_button.disabled = False
        # display(self._file_manager_box)
        self.status_label.value = "Try Again!"
        self.get_file_list(sender)

#==============================================================================
#==================================== STANDARD ================================
class StandardPlot():
    def __init__(self):
        plotly.offline.init_notebook_mode(connected=True)
        self.do_y2_axis = False
        self.go_button_visible = False
        self.go_button = None
        self.main_chart= None
        self.trace_list = []
        self.x_axis_title = "Not Set"
        self.y_axis_title = "Not Set"
        self.y_axis2_title = "Not Set"
        self.chart_title = "Unset Title"
        self.y_axis_options = {}
        self.chart_width = 800
        self.chart_height = 400
        self.full_data = None
        self.time_range = dict
        self.lower_time_limit = '2017-11-07 17:00:00'
        self.upper_time_limit = '2017-11-07 18:00:00'
        self.plot_range_data = None
        self.chart_built = False
        self.layout = None
        self.status_label = widgets.Label()

        #======================================= FILE MANAGER WIDGETS
        self._file_manager_box = widgets.VBox()
        self.file_manager_box = widgets.HBox()
        self.file_list_box = widgets.VBox()
        self.choice_label = widgets.Label('Standard Plot: Expect 1-2 files')
        self.check_for_files_button = widgets.Button(
            description='Check for Files',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Check for The Important ForgeNano Files',
            icon='check'
        )
        self.check_for_files_button.on_click(self.get_file_list)
        self.import_files_button = widgets.Button(
            description='Import Files',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Import These Important Files',
            icon='check'
        )
        self.import_files_button.on_click(self.import_files)
        self.get_file_list('sender')
        self.file_manager_box.children = [self.check_for_files_button, self.import_files_button, self.file_list_box]
        self._file_manager_box.children = [self.choice_label, self.file_manager_box]

        #============================================ TITLE MANAGER WIDGETS
        self.chart_title_entry = widgets.Text(self.chart_title)
        self.xaxis_title_entry = widgets.Text(self.x_axis_title)
        self.yaxis_title_entry = widgets.Text(self.y_axis_title)
        self.yaxis2_title_entry = widgets.Text(self.y_axis2_title)

        self.title_entry_box = widgets.VBox(children=[
            widgets.HBox(children=[widgets.Label('Chart Title:'), self.chart_title_entry]),
            widgets.HBox(children=[widgets.Label('X Axis Title:'), self.xaxis_title_entry]),
            widgets.HBox(children=[widgets.Label('Y Axis Title:'), self.yaxis_title_entry]),
            widgets.HBox(children=[widgets.Label('Y Axis 2 Title:'), self.yaxis2_title_entry]),
        ])

        self.chart_title_entry.observe(self.set_chart_title, names='value')
        self.xaxis_title_entry.observe(self.set_xaxis_title, names='value')
        self.yaxis_title_entry.observe(self.set_yaxis_title, names='value')
        self.yaxis2_title_entry.observe(self.set_yaxis_title, names='value')

        #============================================ TIME RANGE STUFF
        self.time_range_slider = widgets.IntRangeSlider(
            value=[0, 100],
            min=0,
            max=100,
            step=1,
            description='Time Range',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=False
        )

        self.readback_low = widgets.Label('0')
        self.readback_buffer = widgets.Label('  <----->  ')
        self.readback_high = widgets.Label('100')
        self.readback_group = widgets.HBox([self.readback_low, self.readback_buffer, self.readback_high])
        self.time_range_slider.observe(self.on_value_change, names='value')
        self.range_group = widgets.VBox([self.time_range_slider, self.readback_group])

        #=========================================== TRACE MANAGER
        self.reg_col_selection = widgets.Dropdown()
        self.mass_col_selection = widgets.Dropdown()

        self.reg_col_selection.observe(self.auto_set_title_entry, names='value')
        self.mass_col_selection.observe(self.auto_set_title_mass_entry, names='value')

        self.reg_col_name_entry = widgets.Text('Trace Name')
        self.mass_col_name_entry = widgets.Text('Trace Name')
        self.reg_col_add_button = widgets.Button(
            description='Add Regular Trace',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Add Trace',
            icon='check'
        )
        self.reg_col_add_button.on_click(self.add_regular_trace)
        self.reg_entry_group = widgets.HBox([widgets.Label('Trace Name'), self.reg_col_name_entry, self.reg_col_add_button])
        self.reg_add_group = widgets.VBox([self.reg_col_selection, self.reg_entry_group])
        self.mass_col_add_button = widgets.Button(
            description='Add Mass Trace',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Add Mass Trace',
            icon='check'
        )
        self.mass_col_add_button.on_click(self.add_mass_trace)
        self.mass_entry_group = widgets.HBox([widgets.Label('Trace Name'),  self.mass_col_name_entry, self.mass_col_add_button])
        self.mass_add_group = widgets.VBox([self.mass_col_selection, self.mass_entry_group])
        self.delete_trace_button = widgets.Button(
            description='Delete Trace',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Delete This Stupid Trace, cuz it so stooopid',
            icon='check'
        )

        self.delete_trace_button.on_click(self.delete_trace)
        self.delete_trace_selection = widgets.Dropdown()
        self.delete_trace_control = widgets.HBox(children=[widgets.Label('Delete Trace'), self.delete_trace_selection, self.delete_trace_button])
        self.added_trace_list = widgets.VBox()
        self.trace_accordion = widgets.Accordion(children=[self.reg_add_group, self.mass_add_group])
        #self.trace_accordion = widgets.Accordion(children=[self.reg_add_group, self.mass_add_group, self.delete_trace_control])

        self.trace_accordion.set_title(0, 'Regular Traces')
        self.trace_accordion.set_title(1, 'Mass Traces')
        self.trace_accordion.set_title(2, 'Delete/Edit Trace')

        self.build_trace_list()

        self.trace_manager = widgets.HBox(children=[self.trace_accordion, self.added_trace_list])
        self.main_accordion = widgets.Accordion(children=[self.title_entry_box, self.range_group, self.trace_manager])
        self.main_accordion.set_title(0, 'Titles')
        self.main_accordion.set_title(1, 'Data Range')
        self.main_accordion.set_title(2, 'Trace Manager')

        self.go_button = widgets.Button(
            description='Online Chart',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Build a Chart',
            icon='check'
        )

        self.go_button.on_click(self.update_chart)

        self.offline_chart = widgets.Button(
            description='Offline Chart',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Build a Chart',
            icon='check'
        )

        self.offline_chart.on_click(self.offline_plot)

        self.chart_box = widgets.HBox(children=[self.go_button, self.offline_chart])

        display(self._file_manager_box)

    def set_build_box_state(self, state):
        self.go_button.disabled = not state
        self.offline_chart.disabled = not state

    def offline_plot(self, sender):
        self.status_label.value = 'Building Offline Chart... Please Wait'
        self.set_build_box_state(False)
        self.build_layout()
        self.main_chart = graph_objects.Figure(data=self.trace_list, layout=self.layout)
        offline.plot(self.main_chart)
        self.status_label.value = 'Chart Built!'
        self.set_build_box_state(True)

    def update_chart(self, sender):
        self.status_label.value = 'Building Offline Chart... Please Wait'
        self.set_build_box_state(False)
        self.build_layout()
        self.main_chart = graph_objects.Figure(data=self.trace_list, layout=self.layout)
        iplot(self.main_chart)
        self.status_label.value = 'Chart Built!'
        self.set_build_box_state(True)

    def build_layout(self):
        self.layout = Layout(title=self.chart_title,
                             xaxis=dict(title=self.x_axis_title,
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20)),
                             yaxis=dict(title=self.y_axis_title,
                                        showgrid=True,
                                        linecolor='black',
                                        ticks='outside'),
                             margin=dict(t=50),
                             autosize=False,
                             width=self.chart_width,
                             height=self.chart_height)
        if self.do_y2_axis:
            self.layout['yaxis2'] = {'title': self.yaxis2_title_entry.value, 'side': 'right', 'overlaying': 'y', 'exponentformat': 'power'}
        self.layout['legend'] = {'x': 1.15}
        #print('layout built')


    def add_trace(self, key, name):
        #print('def add trace key: %s name: %s' % (key, name))
        self.trace_list.append(graph_objects.Scatter(
            x=self.plot_range_data.index,
            y=self.plot_range_data[key],
            name=name,
            mode='lines',
        ))
        if not self.go_button_visible:
            display(self.chart_box)
            self.go_button_visible = True


    def auto_set_title_mass_entry(self, sender):
        selection = self.mass_col_selection.value
        title = selection.replace('_', '-')
        self.mass_col_name_entry.value = title

    def auto_set_title_entry(self, sender):
        selection = self.reg_col_selection.value
        title = selection.replace('_', '-')
        title = title.upper()
        self.reg_col_name_entry.value = title

    def set_plot_range(self, sender):
        self.plot_range_data = self.full_data.loc[self.lower_time_limit:self.upper_time_limit]

    def set_chart_title(self, sender):
        new_title = self.chart_title_entry.value
        self.chart_title = new_title
        if self.chart_built:
            self.layout.title = new_title

    def set_xaxis_title(self, sender):
        new_title = self.xaxis_title_entry.value
        self.x_axis_title = new_title

    def set_yaxis_title(self, sender):
        new_title = self.yaxis_title_entry.value
        self.y_axis_title = new_title

    def set_yaxis2_title(self, sender):
        new_title = self.yaxis2_title_entry.value
        self.y_axis2_title = new_title


    def delete_trace(self, sender):
        pass

    def add_mass_trace(self, sender):
        key = self.mass_col_selection.value
        name = self.mass_col_name_entry.value
        self.trace_list.append(graph_objects.Scatter(
            x=self.plot_range_data.index,
            y=self.plot_range_data[key],
            connectgaps=True,
            name=name,
            mode='lines',
            yaxis='y2',
        ))
        if not self.go_button_visible:
            display(self.chart_box)
            self.go_button_visible = True
        if not self.do_y2_axis:
            self.do_y2_axis = True
        self.build_trace_list()

    def add_regular_trace(self, sender):
        key = self.reg_col_selection.value
        name = self.reg_col_name_entry.value
        self.add_trace(key, name)
        self.build_trace_list()


    def on_value_change(self, change):
        low = change['new'][0]
        high = change['new'][1]
        if self.full_data is not None:
            lower_string = str(self.full_data.index[low])
            upper_string = str(self.full_data.index[high])
            self.readback_low.value = lower_string
            self.readback_high.value = upper_string
            self.lower_time_limit = lower_string
            self.upper_time_limit = upper_string
            self.set_plot_range('sender')


    def import_files(self, sender):
        self._file_manager_box.close()
        self.status_label.value = 'Importing Files... Please Wait'
        display(self.status_label)
        filename_list = os.listdir('data')
        first = True
        for file_name in filename_list:
            self.status_label.value = 'Importing %s ... Please Wait' % file_name
            filename, extension = os.path.splitext(file_name)
            if extension == '.csv' or extension == '.CSV' or extension == '':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), index_col=0)
            elif extension == '.txt' or extension == '.TXT':
                full_file = "%s/data/%s" % (os.getcwd(), file_name)
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), delimiter='\t', index_col=0)

            else:
                data = None
            if data is not None:
                nindex = []
                for i in data.index:
                    sub = i.split('.')
                    if len(sub) == 1:
                        break
                    _sub = sub[1].split(' ')
                    new_date = "%s %s" % (sub[0], _sub[1])
                    nindex.append(new_date)
                if len(nindex) == len(data.index):
                    data.index = nindex
                try:
                    data.index = pandas.to_datetime(data.index)
                except ValueError:
                    if (extension == '.txt') or (extension == '.TXT'):
                        data = self.digest_file(full_file)
                        data.index = pandas.to_datetime(data.index)
            else:
                #todo handle this shit!
                return
            if first:
                first = False
                self.full_data = data
            else:
                self.full_data = self.full_data.join(data)
        new_columns = []
        for column in self.full_data.columns:
            new_col = column.strip()
            new_columns.append(new_col)
        self.full_data.columns = new_columns
        #print((len(self.full_data.index)-1))
        self.time_range = self.get_time_range()
        self.time_range_slider.max = len(self.full_data.index) - 1
        self.time_range_slider.value = (0, len(self.full_data.index) - 1)

        self.reg_col_list = []
        self.mass_col_list = []

        for column in self.full_data:
            if 'Mass ' in column:
                self.mass_col_list.append(column)
            else:
                self.reg_col_list.append(column)
        self.reg_col_selection.options = self.reg_col_list
        self.mass_col_selection.options = self.mass_col_list
        self.status_label.value = 'Import Complete. Build An Awesome Chart Now!'
        display(self.main_accordion)

    def get_time_range(self):
        if self.full_data is not None:
            result = dict()
            result['lower'] = self.full_data.index[0]
            result['upper'] = self.full_data.index[len(self.full_data.index) - 1]
            return result

    def get_file_list(self, sender):
        file_list = os.listdir('data')
        widget_list = []
        widget_list.append(widgets.Label('Files in Data Directory'))
        if len(file_list) > 0:
            self.import_files_button.disabled = False
            for filename in file_list:
                widget_list.append(widgets.Label(filename))
        elif len(file_list) == 0:
            self.import_files_button.disabled = True
            widget_list.append(widgets.Label('No Files!'))
        self.file_list_box.children = widget_list

    def build_trace_list(self):
        gui_trace_list = []
        if len(self.trace_list) == 0:
            gui_trace_list.append(widgets.Label('No Traces Added'))
        else:
            gui_trace_list.append(widgets.Label('Added Traces'))
            [gui_trace_list.append(widgets.Label(trace.name)) for trace in self.trace_list]
        self.added_trace_list.children = gui_trace_list



    def digest_file(self, file_name):
        self.status_label.value = 'Medusa File Detected... Handling it...'
        mass_list = dict()
        _mass_list = ['time_stamp']
        start_time = None
        start_write = False
        temp_file = os.path.join(os.getcwd(), 'data/temp.csv')
        with open(file_name, 'r') as _file:
            do_loop = True
            build_mass_list = False
            mass_list_done = False
            header_written = False
            loop_count = 1
            while do_loop:
                line = _file.readline()
                if line == '':
                    do_loop = False
                    break
                # Extract the start time and convert to date time object
                if 'Start time' in line:
                    sub = line.split(',')
                    s = sub[2].split("\n")
                    string_start = "%s%s" % (sub[1], s[0])
                    _sub = string_start.split(' ')
                    while '' in _sub: _sub.remove('')
                    f_string = ",".join(_sub)
                    start_time = datetime.strptime(f_string, '%b,%d,%Y,%I:%M:%S,%p')

                items = line.split(' ')
                # Find first line list channel mass relationships
                if items[0] == '1':
                    build_mass_list = True
                # First line after the mass list
                if build_mass_list and items[0] == "\n":
                    build_mass_list = False
                    mass_list_done = True

                # If we're working on the mass list take appropriate action
                if build_mass_list:
                    while '' in items: items.remove('')
                    # sub = items[1].split('.')
                    # name = "Mass %s" % (sub[0])
                    name = items[2]
                    mass_list[items[0]] = name
                    _mass_list.append(name)

                # Header is written, finish it up
                if header_written:
                    if (items[0] != "\n") and (not start_write):
                        start_write = True

                if start_write:
                    while '' in items: items.remove('')
                    items.pop((len(items) - 1))
                    milliseconds = float(items[0].strip(',')) * 1000
                    timestamp = start_time + timedelta(milliseconds=milliseconds)
                    timestamp_string = "%s," % timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    items[0] = timestamp_string
                    items[(len(items) - 1)] = items[(len(items) - 1)].strip(',')
                    line_string = "".join(items)
                    with open(temp_file, '+a') as temp:
                        temp.write("%s\n" % line_string)

                # Start doing crap after the mass list is ready
                if mass_list_done and (not header_written):
                    if items[0] == 'Time(s)':
                        header_string = ','.join(_mass_list)
                        with open(temp_file, '+a') as temp:
                            temp.write("%s\n" % header_string)
                        header_written = True

                loop_count += 1
        data = pandas.read_csv("%s/data/%s" % (os.getcwd(), 'temp.csv'), index_col=0)
        os.remove("%s/data/%s" % (os.getcwd(), 'temp.csv'))
        return data


#==============================================================================
#==================================== OVERLAY =================================
class OverlayPlot():
    def __init__(self):
        plotly.offline.init_notebook_mode(connected=True)
        self.build_box = None
        self.main_chart= None
        self.trace_list = []
        self.x_axis_title = "Not Set"
        self.y_axis_title = "Not Set"
        self.chart_title = "Unset Title"
        self.chart_width = 1000
        self.chart_height = 400
        self.full_data = None
        self.layout = None
        self.reg_col_list = []
        self.status_label = widgets.Label()

        #======================================= FILE MANAGER WIDGETS
        self._file_manager_box = widgets.VBox()
        self.file_manager_box = widgets.HBox()
        self.file_list_box = widgets.VBox()
        self.choice_label = widgets.Label('Overlay Plot: Expecting Exactly 1 file')
        self.check_for_files_button = widgets.Button(
            description='Check for Files',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Check for The Important ForgeNano Files',
            icon='check'
        )
        self.check_for_files_button.on_click(self.get_file_list)
        self.import_files_button = widgets.Button(
            description='Import Files',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Import These Important Files',
            icon='check'
        )
        self.import_files_button.on_click(self.import_files)
        self.get_file_list('sender')
        self.file_manager_box.children = [self.check_for_files_button, self.import_files_button, self.file_list_box]
        self._file_manager_box.children = [self.choice_label, self.file_manager_box]

        #============================================ TITLE MANAGER WIDGETS
        self.chart_title_entry = widgets.Text(self.chart_title)
        self.xaxis_title_entry = widgets.Text(self.x_axis_title)
        self.yaxis_title_entry = widgets.Text(self.y_axis_title)
        #self.yaxis2_title_entry = widgets.Text(self.y_axis2_title)

        self.title_entry_box = widgets.VBox(children=[
            widgets.HBox(children=[widgets.Label('Chart Title:'), self.chart_title_entry]),
            widgets.HBox(children=[widgets.Label('X Axis Title:'), self.xaxis_title_entry]),
            widgets.HBox(children=[widgets.Label('Y Axis Title:'), self.yaxis_title_entry]),
            #widgets.HBox(children=[widgets.Label('Y Axis 2 Title:'), self.yaxis2_title_entry]),
        ])

        self.chart_title_entry.observe(self.set_chart_title, names='value')
        self.xaxis_title_entry.observe(self.set_xaxis_title, names='value')
        self.yaxis_title_entry.observe(self.set_yaxis_title, names='value')
        #self.yaxis2_title_entry.observe(self.set_yaxis_title, names='value')

        #============================================= BREAKUP CHOOSER SHIT
        self.break_choice_entry = widgets.Dropdown(options=self.reg_col_list,
                                                    description='Prec 1:',
                                                    disabled=False,
                                                )

        self.trace_choice_entry = widgets.Dropdown(options=self.reg_col_list,
                                                   description='Plot:',
                                                   disabled=False,
                                                   )

        self.break_choice_box = widgets.HBox(children=[self.break_choice_entry,
                                                       self.trace_choice_entry])
        #=============================================== BUTTON BOX


        self.go_button = widgets.Button(
            description='Go!',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Build a Chart',
            icon='check'
        )

        self.go_button.on_click(self.online_chart)

        self.offline_button = widgets.Button(
            description='New Window',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Build Chart In New Window',
            icon='check'
        )

        self.offline_button.on_click(self.offline_chart)

        self.build_box = widgets.HBox(children=[self.go_button, self.offline_button])

        self.main_accordion = widgets.Accordion(children=[self.title_entry_box, self.break_choice_box])
        self.main_accordion.set_title(0, 'Titles')
        self.main_accordion.set_title(1, 'Break Manager')

        display(self._file_manager_box)

    def set_build_box_state(self, state):
        self.go_button.disabled = not state
        self.offline_button.disabled = not state

    def offline_chart(self, sender):
        self.status_label.value = 'Building Offline Chart... Please Wait'
        self.set_build_box_state(False)
        self.build_chart()
        offline.plot(self.main_chart)
        self.set_build_box_state(True)

#key is the break, xv_102
    def online_chart(self, sender):
        self.status_label.value = 'Building Online Chart... Please Wait'
        self.set_build_box_state(False)
        self.build_chart()
        iplot(self.main_chart)
        self.set_build_box_state(True)

    def build_chart(self):
        key = self.break_choice_entry.value
        #prec2 = self.break2_choice_entry.value
        trace = self.trace_choice_entry.value
        is_tracking = False
        cycle_list = []
        last_a = None
        last_b = None
        for i in range(0, len(self.full_data.index) - 1):
            a = self.full_data[key][i]
            if a == 1:
                if last_a == 0:
                    if is_tracking:
                        d['finish'] = str(self.full_data.index[i-1])
                        cycle_list.append(d)
                        d = dict()
                        d['start'] = str(self.full_data.index[i])
                    else:
                        is_tracking = True
                        d = dict()
                        d['start'] = str(self.full_data.index[i])
            last_a = a
        try:
            x = d['finish']
        except:
            d['finish'] = self.full_data.index[(len(self.full_data.index)-1)]
            cycle_list.append(d)
        data_sets = []
        trace_list = []
        children = []
        for idx, cycle in enumerate(cycle_list):
            row = widgets.HBox(children=[widgets.Label('C%s: ' % str(idx+1)),
                                         widgets.Label('Start: %s  -' % cycle['start']),
                                         widgets.Label('  Finish: %s' % cycle['finish'])])
            children.append(row)
            sub_set = self.full_data.loc[cycle['start']:cycle['finish']]
            ilist = [] #index list
            [ilist.append(idx) for idx in range(0, len(sub_set.index))]
            #reset index so first data point is at index 0 for all subsets
            sub_set.index = ilist
            data_sets.append(sub_set)
            trace_list.append(graph_objects.Scatter(
                x=sub_set.index,
                y=sub_set[trace],
                name=("%s C%s" % (trace, str(idx + 1))),
                mode='lines', ))
        self.build_layout()
        self.main_chart = graph_objects.Figure(data=trace_list, layout=self.layout)
        t_box = widgets.VBox(children=children)
        display(t_box)


    def build_layout(self):
        self.layout = Layout(title=self.chart_title,
                             xaxis=dict(title=self.x_axis_title,
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20)),
                             yaxis=dict(title=self.y_axis_title,
                                        showgrid=True,
                                        linecolor='black',
                                        ticks='outside'),
                             margin=dict(t=50),
                             autosize=False,
                             width=self.chart_width,
                             height=self.chart_height)
        self.layout['legend'] = {'x': 1.15}


    def set_chart_title(self, sender):
        new_title = self.chart_title_entry.value
        self.chart_title = new_title

    def set_xaxis_title(self, sender):
        new_title = self.xaxis_title_entry.value
        self.x_axis_title = new_title

    def set_yaxis_title(self, sender):
        new_title = self.yaxis_title_entry.value
        self.y_axis_title = new_title

    def import_files(self, sender):
        self._file_manager_box.close()
        filename_list = os.listdir('data')
        first = True
        self.status_label.value = 'Importing Files...'
        display(self.status_label)
        for file_name in filename_list:
            self.status_label.value = 'Importing: %s' % file_name
            filename, extension = os.path.splitext(file_name)
            if extension == '.csv' or extension == '.CSV' or extension == '':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), index_col=0)
            elif extension == '.txt' or extension == '.TXT':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), delimiter='\t', index_col=0)
            else:
                data = None
            if data is not None:
                data.index = pandas.to_datetime(data.index)
                # try:
                #     data.index = pandas.to_datetime(data.index)
                # except ValueError:
                #     if (extension == '.txt') or (extension == '.TXT'):
                #         data = self.digest_file(full_file)
                #         data.index = pandas.to_datetime(data.index)
            else:
                #todo handle this shit!
                return
            if first:
                first = False
                self.full_data = data
            else:
                self.full_data = self.full_data.join(data)
        new_columns = []
        for column in self.full_data.columns:
            new_col = column.strip()
            new_columns.append(new_col)
        self.full_data.columns = new_columns
        self.reg_col_list = []
        for column in self.full_data:
                 self.reg_col_list.append(column)

        self.break_choice_entry.options = self.reg_col_list
        self.trace_choice_entry.options = self.reg_col_list
        self.status_label.value = 'Import Complete!'
        display(self.main_accordion)
        display(self.build_box)

    def get_file_list(self, sender):
        file_list = os.listdir('data')
        widget_list = []
        widget_list.append(widgets.Label('Files in Data Directory'))
        if len(file_list) > 0:
            self.import_files_button.disabled = False
            for filename in file_list:
                widget_list.append(widgets.Label(filename))
        elif len(file_list) == 0:
            self.import_files_button.disabled = True
            widget_list.append(widgets.Label('No Files!'))
        self.file_list_box.children = widget_list

    # def digest_file(self, file_name):
    #     self.status_label.value = 'RGA File Detected... Handling it...'
    #     mass_list = dict()
    #     _mass_list = ['time_stamp']
    #     start_time = None
    #     start_write = False
    #     temp_file = os.path.join(os.getcwd(), 'data/temp.csv')
    #     with open(file_name, 'r') as _file:
    #         do_loop = True
    #         build_mass_list = False
    #         mass_list_done = False
    #         header_written = False
    #         loop_count = 1
    #         while do_loop:
    #             line = _file.readline()
    #             if line == '':
    #                 do_loop = False
    #                 break
    #             # Extract the start time and convert to date time object
    #             if 'Start time' in line:
    #                 sub = line.split(',')
    #                 s = sub[2].split("\n")
    #                 string_start = "%s%s" % (sub[1], s[0])
    #                 _sub = string_start.split(' ')
    #                 while '' in _sub: _sub.remove('')
    #                 f_string = ",".join(_sub)
    #                 start_time = datetime.strptime(f_string, '%b,%d,%Y,%I:%M:%S,%p')

    #             items = line.split(' ')
    #             # Find first line list channel mass relationships
    #             if items[0] == '1':
    #                 build_mass_list = True
    #             # First line after the mass list
    #             if build_mass_list and items[0] == "\n":
    #                 build_mass_list = False
    #                 mass_list_done = True

    #             # If we're working on the mass list take appropriate action
    #             if build_mass_list:
    #                 while '' in items: items.remove('')
    #                 # sub = items[1].split('.')
    #                 # name = "Mass %s" % (sub[0])
    #                 name = items[2]
    #                 mass_list[items[0]] = name
    #                 _mass_list.append(name)

    #             # Header is written, finish it up
    #             if header_written:
    #                 if (items[0] != "\n") and (not start_write):
    #                     start_write = True

    #             if start_write:
    #                 while '' in items: items.remove('')
    #                 items.pop((len(items) - 1))
    #                 milliseconds = float(items[0].strip(',')) * 1000
    #                 timestamp = start_time + timedelta(milliseconds=milliseconds)
    #                 timestamp_string = "%s," % timestamp.strftime("%Y-%m-%d %H:%M:%S")
    #                 items[0] = timestamp_string
    #                 items[(len(items) - 1)] = items[(len(items) - 1)].strip(',')
    #                 line_string = "".join(items)
    #                 with open(temp_file, '+a') as temp:
    #                     temp.write("%s\n" % line_string)

    #             # Start doing crap after the mass list is ready
    #             if mass_list_done and (not header_written):
    #                 if items[0] == 'Time(s)':
    #                     header_string = ','.join(_mass_list)
    #                     with open(temp_file, '+a') as temp:
    #                         temp.write("%s\n" % header_string)
    #                     header_written = True

    #             loop_count += 1
    #     data = pandas.read_csv("%s/data/%s" % (os.getcwd(), 'temp.csv'), index_col=0)
    #     os.remove("%s/data/%s" % (os.getcwd(), 'temp.csv'))
    #     return data



#==============================================================================
#==================================== KWIK PLOT ===============================
class KwikPlot():
    def __init__(self):
        self.status_label = widgets.Label()
        self.trace_list = []
        # ======================================= FILE MANAGER WIDGETS
        self._file_manager_box = widgets.VBox()
        self.file_manager_box = widgets.HBox()
        self.file_list_box = widgets.VBox()
        self.choice_label = widgets.Label('Kwik Plot: Expecting 1 file from Pluto ONLY')
        self.check_for_files_button = widgets.Button(
            description='Check for Files',
            disabled=False,
            button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Check for The Important ForgeNano Files',
            icon='check'
        )
        self.check_for_files_button.on_click(self.get_file_list)
        self.import_files_button = widgets.Button(
            description='Import Files',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Import These Important Files',
            icon='check'
        )
        self.import_files_button.on_click(self.import_files)
        self.get_file_list('sender')
        self.file_manager_box.children = [self.check_for_files_button, self.import_files_button, self.file_list_box]
        self._file_manager_box.children = [self.choice_label, self.file_manager_box]

        display(self._file_manager_box)

    def get_file_list(self, sender):
        file_list = os.listdir('data')
        widget_list = []
        widget_list.append(widgets.Label('Files in Data Directory'))
        if len(file_list) > 0:
            self.import_files_button.disabled = False
            for filename in file_list:
                widget_list.append(widgets.Label(filename))
        elif len(file_list) == 0:
            self.import_files_button.disabled = True
            widget_list.append(widgets.Label('No Files!'))
        self.file_list_box.children = widget_list

    def import_files(self, sender):
        self._file_manager_box.close()
        self.status_label.value = 'Importing Files... Please Wait'
        display(self.status_label)
        filename_list = os.listdir('data')
        first = True
        for file_name in filename_list:
            self.status_label.value = 'Importing %s ... Please Wait' % file_name
            filename, extension = os.path.splitext(file_name)
            if extension == '.csv' or extension == '.CSV' or extension == '':
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), index_col=0)
            elif extension == '.txt' or extension == '.TXT':
                full_file = "%s/data/%s" % (os.getcwd(), file_name)
                data = pandas.read_csv("%s/data/%s" % (os.getcwd(), file_name), delimiter='\t', index_col=0)

            else:
                data = None

            if data is not None:
                data.index = pandas.to_datetime(data.index)

            if first:
                first = False
                self.full_data = data
            else:
                self.full_data = self.full_data.join(data)

            new_columns = []
            for column in self.full_data.columns:
                new_col = column.strip()
                new_columns.append(new_col)
            self.full_data.columns = new_columns

        keyset_1 = ['pt_100', 'pt_601']
        keyset_2 = ['PT-Exhaust', 'PT-Manifold']

        try:
            for key in keyset_1:
                _key = key.replace('_', ' ')
                _key = _key.upper()
                self.add_trace(key, _key)
        except:
            for key in keyset_2:
                _key = key.replace('_', ' ')
                _key = _key.upper()
                self.add_trace(key, _key)

        self.layout = Layout(title='Kwik Plot',
                             xaxis=dict(title='Time',
                                        showgrid=False,
                                        linecolor='black',
                                        ticks='outside',
                                        titlefont=dict(size=20)),
                             yaxis=dict(title='Pressure',
                                        showgrid=True,
                                        linecolor='black',
                                        ticks='outside'),
                             margin=dict(t=50),
                             autosize=False,
                             width=1000,
                             height=800)

        self.main_chart = graph_objects.Figure(data=self.trace_list, layout=self.layout)
        self.status_label.value = 'Chart Built!'
        offline.plot(self.main_chart)

    def add_trace(self, key, name):
        self.trace_list.append(graph_objects.Scatter(
            x=self.full_data.index,
            y=self.full_data[key],
            name=name,
            mode='lines',
        ))