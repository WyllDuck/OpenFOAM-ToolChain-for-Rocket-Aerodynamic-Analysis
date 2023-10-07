FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# setup timezone
ENV TZ=Europe/Copenhagen
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install essentials
RUN apt-get update -y
RUN apt-get install -y ssh
RUN apt-get install -y curl
RUN apt-get install -y nano
RUN apt-get install -y git
RUN apt-get install -y htop
RUN apt-get install -y build-essential
RUN apt-get install -y software-properties-common

RUN apt-get install -y python3-pip
RUN pip install jinja2-cli
		
# install useful openfoam tools
RUN apt-get install -y ffmpeg

# download openfoam and update repos
RUN curl https://dl.openfoam.com/add-debian-repo.sh | bash
RUN apt-get update

# install latest openfoam
RUN apt-get install -y openfoam-default

# add user "foam"
RUN useradd --user-group --create-home --shell /bin/bash foam ;\
	echo "foam ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    
# source openfoam and fix docker mpi
RUN echo "source /usr/lib/openfoam/openfoam/etc/bashrc" >> ~foam/.bashrc ;\
   echo "export OMPI_MCA_btl_vader_single_copy_mechanism=none" >> ~foam/.bashrc

# change environmental variables to make sure $WM_PROJECT_USER_DIR is outside of the container
RUN sed -i '/export WM_PROJECT_USER_DIR=/cexport WM_PROJECT_USER_DIR="/data/foam-$WM_PROJECT_VERSION"' /usr/lib/openfoam/openfoam/etc/bashrc

# change user to "foam"
USER foam

