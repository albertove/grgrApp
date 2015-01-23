from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from grgrSIte.grgrApp.models import RegistrationForm, LoginForm, Project, ProjectParameter, ProjectTraffic,ProjectStormwater,ProjectSummary
from grgrSIte.grgrApp.models import ProjectForm, ParameterForm, TrafficForm, StormwaterForm, SummaryForm
from django.contrib.auth.decorators import login_required
import calculations
from django import forms
#from django.contrib.auth.decorators import login_required

def index_view(request):
    #users_list = User.objects.all()
    context={'web_app':'Welcome to GrGr App'}
    return render(request,'grgrApp/index.html',context)# Create your views here.


def users_view(request):
    users_list = User.objects.all()
    context = {'users_list':users_list}
    return render(request,'grgrApp/users.html',context)


def registration_view(request):
    errors = []
    form = RegistrationForm()
    if request.method == 'POST':
        """
        if not request.POST.get('username',''):
            errors.append("Please enter a username.")
        if not request.POST.get('name',''):
            errors.append("Please, write your first name.")
        if not request.POST.get('lastname',''):
            errors.append("Please, write your last name.")
        if not errors:
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            fusername = form.cleaned_data['username']
            try:
                u = User.objects.get(username=fusername)
                errors.append('The username %s is already used. Please, try a new username.' %fusername)
            except User.DoesNotExist:
                fname = form.cleaned_data['name']
                flastname = form.cleaned_data['lastname']
                passw  = fusername + fname
                u = User.objects.create_user(username=fusername,password=passw,first_name=fname,last_name=flastname)
                u.save()
                return HttpResponseRedirect('grgrApp/thanks.html')
    else:
        form = RegistrationForm()

    return render(request, 'grgrApp/registration.html',{
        'errors': errors,
        'username': request.POST.get('username',''),
        'name': request.POST.get('name',''),
        'lastname': request.POST.get('lastname',''),
        'form':form,
    })

def login_view(request):
    errors = []
    if request.user.is_authenticated():
        context = {'user_name':request.user.first_name,'message':'You have already logged in.'}
        return render(request,'grgrApp/loginerror.html',context)
    form = LoginForm()
    if request.method == 'POST':
        """
        if not request.POST.get('username', ''):
            errors.append('Enter your username.')
        if not request.POST.get('name', ''):
            errors.append('Enter your first name.')
        if not errors:
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            fusername = form.cleaned_data['username']
            fname = form.cleaned_data['name']
            u = authenticate(username=fusername, password=fusername+fname)
            if u is not None:
                if u.is_active:
                    login(request,u)
                    request.session['loginuser'] = u.username
                    # context = {'form':ProjectForm}
                    return HttpResponseRedirect('/grgrApp/project/')
                    # return render(request,'grgrApp/project.html',context)
            else:
                errors.append("The username or first name are wrong. Please try again!")
                errors.append("Are you already resgistered? If not, please register before login.")
    else:
        form = LoginForm()

    return render(request, 'grgrApp/login.html',{
        'errors': errors,
        'username': request.POST.get('username',''),
        'name': request.POST.get('name',''),
        'form':form,
    })

def logout_view(request):
    logout(request)
    return render(request,'grgrApp/logout.html')


def project_view(request):
    errors = []
    #form = ProjectForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            context = {'form':ParameterForm}
            if form.is_valid():
                fprname = form.cleaned_data['prname']
                #project = Project.objects.get(prname=fprname)
                try:
                    project = Project.objects.get(prname=fprname)
                    #print project.prname
                    #print "Project already exist"
                    request.session['projectname'] = project.prname
                    form = ProjectForm(request.POST,instance=project)
                    form.save()
                except:
                    #print "New project!"
                    user = User.objects.get(username=request.session['loginuser'])
                    #print user
                    request.session['projectname'] = fprname
                    prnew = Project(user=user,prname=fprname)
                    form = ProjectForm(request.POST,instance=prnew)
                    form.save()
                return HttpResponseRedirect('/grgrApp/parameter/')
            else:
                return render(request, 'grgrApp/project.html',{'errors': errors,'form':form})
        else:
            try:
                fprname = request.session['projectname']
                #print fprname
                project = Project.objects.get(prname=fprname)
                form = ProjectForm(instance=project)
            except:
                form = ProjectForm()
            return render(request, 'grgrApp/project.html',{'errors': errors,'form':form,})
    else:
        return render(request,'grgrApp/login.html',{'form':LoginForm})


def parameter_view(request):
    errors = []
    #form = ProjectForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ParameterForm(request.POST)
            context = {'form':TrafficForm}
            if form.is_valid():
                project = Project.objects.get(prname=request.session['projectname'])
                try:
                    parameter = ProjectParameter.objects.get(project=project)
                    form = ParameterForm(request.POST,instance=parameter)
                    form.save()
                except:
                    parameternew = ProjectParameter(project=project,application=1,type_of_paving=1,conv_paving=0,conc_paving_joint=0,riven_paving=0)
                    form = ParameterForm(request.POST,instance=parameternew)
                    form.save()
                #return render(request,'grgrApp/traffic.html',context)
                return HttpResponseRedirect('/grgrApp/traffic/')
            else:
                return render(request, 'grgrApp/parameter.html',{'errors': errors,'form':form,})
        else:

            try:
                fprname = request.session['projectname']
                #print fprname
                project = Project.objects.get(prname=fprname)
                parameter = ProjectParameter.objects.get(project=project)
                #form = ParameterForm(project=project,application=parameter.application,type_of_paving=parameter.type_of_paving, conv_paving=parameter.conv_paving,conc_paving_joint=parameter.conc_paving_joint,riven_paving=parameter.riven_paving)
                form = ParameterForm(instance=parameter)
                print form
            except:
                form = ParameterForm()
            #return render(request, 'grgrApp/project.html',{'errors': errors,'form':form,})
            #form = ParameterForm()
            return render(request, 'grgrApp/parameter.html',{'errors': errors,'form':form,})
    else:
        return render(request,'grgrApp/login.html',{'form':LoginForm})

def traffic_view(request):
    errors = []
    #form = ProjectForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = TrafficForm(request.POST)
            if form.is_valid():
                form.data = form.data.copy()
                try:
                    thickness_sub_layer = float(form.data.get('thickness_subbase_layer'))
                    fraction_sub_layer = float(form.data.get('fraction_subbase_layer'))
                except:
                    thickness_sub_layer = form.data.get('thickness_subbase_layer')
                    fraction_sub_layer = form.data.get('fraction_subbase_layer')
                # print fraction_sub_layer
                if "update_values" in form.data:
                #if (thickness_sub_layer == 0) or (thickness_sub_layer == None) or (fraction_sub_layer == 0) or (fraction_sub_layer == None):
                    #print form.changed_data()
                    # print 1
                    # Data from form
                    traffic_category = form.data.get('traffic_category')
                    subgrade_material = form.data.get('subgrade_material')
                    subbase_material = form.data.get('subbase_material')
                    climatic_zone = form.data.get('climatic_zone')
                    frost_class = form.data.get('frost_suceptibility_class')
                    thick_surface_course = form.data.get('thickness_surface_course')
                    thick_bedding_layer = form.data.get('thickness_bedding_layer')
                    # Calculations
                    thickness_base_layer = float(calculations.thicknessBaseLayer(int(traffic_category)))
                    thickness_sub_layer = calculations.thicknessSubbaseLayer(int(subgrade_material),int(traffic_category),int(subbase_material))
                    total_thickness,thickness_sub_layer,fraction_sub_layer = calculations.totalThickness(float(thickness_sub_layer),float(thickness_base_layer),int(climatic_zone),int(frost_class),float(thick_surface_course),float(thick_bedding_layer))
                    form.data['thickness_subbase_layer'] = thickness_sub_layer
                    form.data['fraction_subbase_layer'] = fraction_sub_layer
                    #form.fields['thickness_subbase_layer'] = forms.FloatField("Thickness subbase layer",required=True)
                    #form.fields['fraction_subbase_layer'] = forms.CharField(label="Fraction subbase layer",max_length=4,required=True)
                    #form = TrafficForm(initial={'thickness_subbase_layer':thickness_sub_layer})
                    form.update_values(thickness_sub_layer,fraction_sub_layer)
                    #form.cleaned_data['thickness_subbase_layer'] = thickness_sub_layer
                    #form.cleaned_data['thickness_subbase_layer'] = thickness_sub_layer
                    #form.fields['thickness_subbase_layer'].widget.attrs.update({'class':'labelshort'})
                    context = {'form':form}
                    return render(request,'grgrApp/traffic.html',context)
                else:
                    project = Project.objects.get(prname=request.session['projectname'])
                    try:
                        traffic = ProjectTraffic.objects.get(project=project)
                        form = TrafficForm(request.POST,instance=traffic)
                        form.save()
                    except:
                        trafficnew = ProjectTraffic(project=project,traffic_category=0,thickness_base_layer=0,fraction_base_layer="0/32",thickness_surface_course=0, thickness_bedding_layer=0,
                                                    fraction_bedding_layer="2/4",subgrade_material=0,climatic_zone=0,frost_suceptibility_class=0,subbase_material=0)
                        form = TrafficForm(request.POST,instance=trafficnew)
                        form.save()
                    #context = {'form':StormwaterForm}
                    #return render(request,'grgrApp/stormwater.html',context)
                    return HttpResponseRedirect('/grgrApp/stormwater/')
            else:
                return render(request, 'grgrApp/traffic.html',{'errors': errors,'form':form,})
        else:
            try:
                fprname = request.session['projectname']
                # print fprname
                projec = Project.objects.get(prname=fprname)
                traffic = ProjectTraffic.objects.get(project=projec)
                #print traffic
                form = TrafficForm(instance=traffic)
            except:
                form = TrafficForm()
            return render(request, 'grgrApp/traffic.html',{'errors': errors,'form':form,})
    else:
        return render(request,'grgrApp/login.html',{'form':LoginForm})

def stormwater_view(request):
    errors = []
    #form = ProjectForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = StormwaterForm(request.POST)
            if form.is_valid():
                form.data = form.data.copy()
                #form.save()
                if "storm_update_value" in form.data:
                    depth_draining_pipe = float(form.data.get('depth_draining_pipe'))
                    ground_water_level = float(form.data.get('ground_water_level'))
                    project = Project.objects.get(prname=request.session['projectname'])
                    traffic = ProjectTraffic.objects.get(project=project)
                    thickness_surface_course = traffic.thickness_surface_course
                    thickness_bedding_layer = traffic.thickness_bedding_layer
                    thickness_base_layer = traffic.thickness_base_layer
                    thickness_subbase_layer = traffic.thickness_subbase_layer
                    rest_depth = float(thickness_surface_course) + float(thickness_bedding_layer) + float(thickness_base_layer) + float(thickness_subbase_layer)

                    if depth_draining_pipe > rest_depth:
                        errors.append(u'The depth may not exceed %d to be located within the the sub base layer. Respecify depth.' % rest_depth)
                        depth_draining_pipe = 0
                    else:
                        depth_draining_pipe = depth_draining_pipe

                    #if ground_water_level > rest_depth:
                    #    errors.append(u'The ground water level may not exceed %d to be located within the the sub base layer. Respecify ground water level.' % rest_depth)
                    #    ground_water_level = 0
                    #else:
                    ground_water_level = ground_water_level
                    form.data['depth_draining_pipe'] = depth_draining_pipe
                    form.data['ground_water_level'] = ground_water_level
                    return render(request,'grgrApp/stormwater.html',{'errors':errors,'form':form})
                else:
                    project = Project.objects.get(prname=request.session['projectname'])
                    try:
                        stormwater = ProjectStormwater.objects.get(project=project)
                        form = StormwaterForm(request.POST,instance=stormwater)
                        form.save()
                    except:
                        stormwaternew = ProjectStormwater(project=project,construction_type=0)
                        form = StormwaterForm(request.POST,instance=stormwaternew)
                        form.save()
                    return HttpResponseRedirect('/grgrApp/summary/')
                    #context = {'form':SummaryForm}
                    #summaryform = populate_summaryform(request)
                    #return render(request,'grgrApp/summary.html',{'form':summaryform})
                #context = {'form':ProjectForm}
                #return render(request,'grgrApp/project.html',context)
        else:
            try:
                fprname = request.session['projectname']
                # print fprname
                projec = Project.objects.get(prname=fprname)
                stormwater = ProjectStormwater.objects.get(project=projec)
                #print 2
                print stormwater.construction_type
                form = StormwaterForm(instance=stormwater)
            except:
                form = StormwaterForm()
            return render(request, 'grgrApp/stormwater.html',{'errors': errors,'form':form,})

    else:
        return render(request,'grgrApp/login.html',{'form':LoginForm})


def summary_view(request):
    errors = []
    # print "Summary view"
    if request.user.is_authenticated():
        if request.method == 'POST':
            # print 1
            return HttpResponseRedirect('/grgrApp/project/')
        else:
            # print 2

            dict_type_paving = ['Asphalt or concrete paving blocks','Permeable concrete paving blocks','Riven paving']
            dict_traffic = ['G/C','0 Terrass 1','0 Terrass 2-5','1','2']
            dict_grad_material = ['Material 1','Material 2','Material 3','Material 4','Material 5']
            dict_climatic_zone = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5']
            dict_frost_class = ['3','4']
            dict_base_material = ['Crushed rock','Other than crushed rock']
            dict_const_type = ['None','Biofilter with plants','Biofilter with tree','Infiltration ditch with macadam','Open ditch']

            project = Project.objects.get(prname=request.session['projectname'])
            parameter = ProjectParameter.objects.get(project=project)
            traffic = ProjectTraffic.objects.get(project=project)
            stormwater = ProjectStormwater.objects.get(project=project)

            pavement_area = stormwater.pavement_area #D11
            type_paving = parameter.type_of_paving #D12
            num_draining_pipe = stormwater.num_draining_pipes #D13
            thick_surf_course = traffic.thickness_surface_course #D14
            thick_bedding_layer = traffic.thickness_bedding_layer #D15
            thick_base_layer = traffic.thickness_base_layer #D16
            thick_subbase_layer = traffic.thickness_subbase_layer #D17
            depth_draining  = thick_surf_course + thick_bedding_layer +  thick_base_layer + thick_subbase_layer - stormwater.depth_draining_pipe #D19
            ground_water = stormwater.ground_water_level - (thick_surf_course + thick_bedding_layer +  thick_base_layer + thick_subbase_layer) #D18

            str_type_paving = "%s, h1 = %3.1f [mm]"%(dict_type_paving[type_paving - 1],thick_base_layer)
            str_bedding_layer = "2/4, h2 = %3.1f [mm]"%thick_bedding_layer
            str_unbound_base_layer = "0/32, h3 = %3.1f [mm]"%thick_surf_course
            str_subbase_layer = "h4 = %3.1f [mm]"%(thick_subbase_layer)
            str_thick_subbase_layer = "h4a = %3.1f [mm]"%(thick_subbase_layer - depth_draining)
            str_depth_draining_pipe = "h4b = %3.1f [mm]"%(depth_draining)
            str_distance_ground = "h5 = %3.1f [mm]"%ground_water
            str_type_paving = "%s, h1 = %3.2f [mm]"%(dict_type_paving[type_paving - 1],thick_surf_course)
            str_bedding_layer = "2/4, h2 = %3.2f [mm]"%thick_bedding_layer
            str_unbound_base_layer = "0/32, h3 = %3.2f [mm]"%thick_base_layer
            str_type_paving = "%s, h1 = %3.2f [mm]"%(dict_type_paving[type_paving - 1],thick_base_layer)
            str_bedding_layer = "2/4, h2 = %3.2f [mm]"%thick_bedding_layer
            str_unbound_base_layer = "0/32, h3 = %3.2f [mm]"%thick_surf_course
            str_subbase_layer = "h4 = %3.2f [mm]"%(thick_subbase_layer)
            str_thick_subbase_layer = "h4a = %3.2f [mm]"%(thick_subbase_layer - depth_draining)
            str_depth_draining_pipe = "h4b = %3.2f [mm]"%(depth_draining)
            str_distance_ground = "h5 = %3.2f [mm]"%ground_water

            traffic_class = traffic.traffic_category
            subgrade_material = traffic.subgrade_material
            climatic_zone = traffic.climatic_zone
            frost_class = traffic.frost_suceptibility_class

            const_type = stormwater.construction_type
            height_open_volume = stormwater.height_open_volume #R13
            distance_overflow = stormwater.distance_overflow #R22
            thickness_vegetation_layer = stormwater.thickness_vegetation_layer #R14
            thickness_coarse_sand = stormwater.thickness_coarse_sand #R15
            thickness_coarse_aggregate_26 = stormwater.thickness_coarse_aggregate_26 #R16
            thickness_coarse_aggregate_416 = stormwater.thickness_coarse_aggregate_416 # R17
            #thickness_coarse_aggregate_1632 = 0 #stormwater.thickness_coarse_aggregate_1632 #R18
            #thickness_skeletal_soil = 0 #stormwater.thickness_skeletal_soil #R19
            position_draining_pipe_ditch = stormwater.depth_draining_pipe_bio #R21
            #ground_water_level_ditch = stormwater.ground_water_level_bio #R20


            if type_paving == 1:
                coeff_infiltration = parameter.conv_paving #D38
            elif type_paving == 2:
                coeff_infiltration = parameter.conc_paving_joint #D38
            elif type_paving == 3:
                coeff_infiltration = parameter.riven_paving #D38
            #print pavement_area,type_paving

            variables = [pavement_area,type_paving,num_draining_pipe,thick_surf_course,thick_bedding_layer,thick_base_layer,thick_subbase_layer,ground_water,depth_draining,coeff_infiltration,
                        height_open_volume,thickness_vegetation_layer,thickness_coarse_sand,thickness_coarse_aggregate_26,thickness_coarse_aggregate_416,position_draining_pipe_ditch,distance_overflow]

            DData = calculations.DData(variables)
            str_desing_duration_rain = "%3d [min]"%DData[0]
            str_design_intensity_rain = "%3d [l/s/ha]"%DData[9]
            str_available_volume = "%3d"%DData[1]
            str_required_volume = "%3.1f"%DData[2]

            str_height_open_volume = "h7 = %3d [mm]"%height_open_volume
            str_dist_overflow = "h7b = %3d [mm]"%distance_overflow
            str_vegetation_layer = "h8 = %3d [mm]"%thickness_vegetation_layer
            str_thick_coarse_sand = "h9 = %3d [mm]" %thickness_coarse_sand
            str_thick_aggr_26 = "h10 = %3d [mm]"%thickness_coarse_aggregate_26
            str_thick_aggr_416 = "h11 = %3d [mm]"%thickness_coarse_aggregate_416
            str_thick_skeletal_soil = "h13 = 0 [mm]"
            str_pos_draining_pipe = "h15 = %3d [mm]"%position_draining_pipe_ditch
            str_ground_water_level = "h14 = 0 [mm]"
            str_design_duration_rain_ditch = "%3d [min]"%DData[5]
            str_design_intensity_rain_ditch = "%3d [l/s/ha]"%DData[10]
            str_available_volume_ditch = "%3d [l]"%DData[6]
            str_required_volume_ditch = "%3d [l]"%DData[7]
            print DData[10]

            if DData[3] == 'nej':
                if DData[4] == 'ja':
                    veredict1 = "The construction can manage the required storm water volume."
                elif DData[4] == 'nej':
                    veredict1 = "The construction can manage the required storm water volume and there is no need for the draining pipes."
            else:
                veredict1 = "The construction cannot manage the required storm water volume. The number of draining pipes and/or the thickness of the sub base layer needs to be increased."
            # print thick_subbase_layer
            if DData[8] == 'ja':
                veredict2 = "The construction can manage the required storm water volume."
            elif DData[8] == 'nej':
                veredict2 = "The construction cannot manage the required storm water volume. The area or the thickness of the layers in the storm water construction need to be increased."
            else:
                veredict2 = ""


            sumarynew = ProjectSummary(project=project,sum_type_paving=str_type_paving, sum_bedding_layer = str_bedding_layer,sum_unbound_base_layer=str_unbound_base_layer,
                                sum_sub_base_layer = str_subbase_layer, sum_thickness_subbase_layer = str_thick_subbase_layer, sum_position_draining_pipe = str_depth_draining_pipe,
                                sum_ground_water_level = str_distance_ground,
                                sum_traffic_class = dict_traffic[traffic_class - 1],sum_prepared_subgrade_material = dict_grad_material[subgrade_material - 1],
                                sum_climatic_zone = dict_climatic_zone[climatic_zone - 1],sum_frost_suceptibility_class = dict_frost_class[frost_class - 1],
                                sum_design_duration_rain = str_desing_duration_rain,sum_design_intensity_rain = str_design_intensity_rain,sum_available_volume=str_available_volume,sum_required_volume = str_required_volume,
                                sum_veredict = veredict1,
                                sum_construction_type = dict_const_type[const_type],sum_height_open_volume=str_height_open_volume,
                                sum_distance_overflow = str_dist_overflow,sum_thickness_vegetation_layer=str_vegetation_layer, sum_thickness_coarse_sand=str_thick_coarse_sand,
                                sum_thickness_coarse_aggregate_26=str_thick_aggr_26,sum_thickness_coarse_aggregate_416=str_thick_aggr_416,
                                sum_thickness_skeletal_soil=str_thick_skeletal_soil,
                                sum_position_draining_pipe_ditch=str_pos_draining_pipe,sum_ground_water_level_ditch=str_ground_water_level,sum_design_duration_rain_ditch=str_design_duration_rain_ditch,
                                sum_available_volume_ditch=str_available_volume_ditch,sum_required_volume_ditch=str_required_volume_ditch,sum_veredict_ditch = veredict2,sum_design_intensity_rain_ditch = str_design_intensity_rain_ditch)

            form = SummaryForm(instance=sumarynew)
            return render(request,'grgrApp/summary.html',{'form':form})
    else:
        return render(request,'grgrApp/login.html',{'form':LoginForm})

    return render(request, 'grgrApp/summary.html',{
        'errors': errors,
        'form':form,
    })

def populate_summaryform(request):
    project = Project.objects.get(prname=request.session['projectname'])
    parameter = ProjectParameter.objects.get(project=project)
    traffic = ProjectTraffic.objects.get(project=project)
    stormwater = ProjectStormwater.objects.get(project=project)

    pavement_area = stormwater.pavement_area #D11
    type_paving = parameter.type_of_paving #D12
    num_draining_pipe = stormwater.num_draining_pipes #D13
    thick_surf_course = traffic.thickness_surface_course #D14
    thick_bedding_layer = traffic.thickness_bedding_layer #D15
    thick_base_layer = traffic.thickness_base_layer #D16
    thick_subbase_layer = traffic.thickness_subbase_layer #D17
    #depth_draining  = stormwater.depth_draining_pipe #D19
    depth_draining  = thick_surf_course + thick_bedding_layer +  thick_base_layer + thick_subbase_layer - stormwater.depth_draining_pipe #D19
    ground_water = stormwater.ground_water_level - (thick_surf_course + thick_bedding_layer +  thick_base_layer + thick_subbase_layer) #D18

    traffic_class = traffic.traffic_category
    subgrade_material = traffic.subgrade_material
    climatic_zone = traffic.climatic_zone
    frost_class = traffic.frost_suceptibility_class

    const_type = stormwater.construction_type
    height_open_volume = stormwater.height_open_volume #R13
    distance_overflow = stormwater.distance_overflow #R22
    thickness_vegetation_layer = stormwater.thickness_vegetation_layer #R14
    thickness_coarse_sand = stormwater.thickness_coarse_sand #R15
    thickness_coarse_aggregate_26 = stormwater.thickness_coarse_aggregate_26 #R16
    thickness_coarse_aggregate_416 = stormwater.thickness_coarse_aggregate_416 # R17
    thickness_coarse_aggregate_1632 = 0 #stormwater.thickness_coarse_aggregate_1632 #R18
    thickness_skeletal_soil = 0 #stormwater.thickness_skeletal_soil #R19
    position_draining_pipe_ditch = stormwater.depth_draining_pipe_bio #R21
    ground_water_level_ditch = 0 # stormwater.ground_water_level_bio #R20


    if type_paving == 1:
        coeff_infiltration = parameter.conv_paving #D38
    elif type_paving == 2:
        coeff_infiltration = parameter.conc_paving_joint #D38
    elif type_paving == 3:
        coeff_infiltration = parameter.riven_paving #D38
    #print pavement_area,type_paving

    variables = [pavement_area,type_paving,num_draining_pipe,thick_surf_course,thick_bedding_layer,thick_base_layer,thick_subbase_layer,ground_water,depth_draining,coeff_infiltration,
                height_open_volume,thickness_vegetation_layer,thickness_coarse_sand,thickness_coarse_aggregate_26,thickness_coarse_aggregate_416,position_draining_pipe_ditch,distance_overflow]
    DData = calculations.DData(variables)

    dict_type_paving = ['Asphalt or concrete paving blocks','Permeable concrete paving blocks','Riven paving']
    dict_traffic = ['G/C','0 Terrass 1','0 Terrass 2-5','1','2']
    dict_grad_material = ['Material 1','Material 2','Material 3','Material 4','Material 5']
    dict_climatic_zone = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5']
    dict_frost_class = ['3','4']
    dict_base_material = ['Crushed rock','Other than crushed rock']
    dict_const_type = ['None','Biofilter with plants','Biofilter with tree','Infiltration ditch with macadam','Open ditch']

    if DData[3] == 'nej':
        if DData[4] == 'ja':
            veredict1 = "The construction can manage the required storm water volume."
        elif DData[4] == 'nej':
            veredict1 = "The construction can manage the required storm water volume and there is no need for the draining pipes."
    else:
        veredict1 = "The construction cannot manage the required storm water volume. The number of draining pipes and/or the thickness of the sub base layer needs to be increased."
    # print thick_subbase_layer
    if DData[8] == 'ja':
        veredict2 = "The construction can manage the required storm water volume."
    elif DData[8] == 'nej':
        veredict2 = "The construction cannot manage the required storm water volume. The area or the thickness of the layers in the storm water construction need to be increased."
    else:
        veredict2 = ""


    sumarynew = ProjectSummary(project=project,sum_type_paving=dict_type_paving[type_paving - 1], sum_sub_base_layer = thick_base_layer,
                        sum_thickness_subbase_layer = thick_subbase_layer - depth_draining,
                        sum_position_draining_pipe = depth_draining,sum_ground_water_level = ground_water,
                        sum_traffic_class = dict_traffic[traffic_class - 1],sum_prepared_subgrade_material = dict_grad_material[subgrade_material - 1],
                        sum_climatic_zone = dict_climatic_zone[climatic_zone - 1],sum_frost_suceptibility_class = dict_frost_class[frost_class - 1],
                        sum_design_duration_rain = DData[0],sum_design_intensity_rain = DData[9],sum_available_volume=DData[1],sum_required_volume = DData[2],
                        sum_design_intensity_rain_ditch = DData[10],
                        sum_veredict = veredict1, sum_construction_type = dict_const_type[const_type],sum_height_open_volume=height_open_volume,
                        sum_distance_overflow = distance_overflow,sum_thickness_vegetation_layer=thickness_vegetation_layer, sum_thickness_coarse_sand=thickness_coarse_sand,
                        sum_thickness_coarse_aggregate_26=thickness_coarse_aggregate_26,sum_thickness_coarse_aggregate_416=thickness_coarse_aggregate_416,
                        sum_thickness_coarse_aggregate_1632=0,sum_thickness_skeletal_soil=0,
                        sum_position_draining_pipe_ditch=position_draining_pipe_ditch,sum_ground_water_level_ditch=0,sum_design_duration_rain_ditch=DData[5],
                        sum_available_volume_ditch=DData[6],sum_required_volume_ditch=DData[7],sum_veredict_ditch = veredict2)

    form = SummaryForm(instance=sumarynew)
    return form