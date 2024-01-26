FROM jenkins/jenkins:2.426.1-jdk17
USER root
RUN apt-get update &amp;&amp; apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
https://download.docker.com/linux/debian/gpg
RUN echo &quot;deb [arch=$(dpkg --print-architecture) \
signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
https://download.docker.com/linux/debian \
$(lsb_release -cs) stable&quot; &gt; /etc/apt/sources.list.d/docker.list
RUN apt-get update &amp;&amp; apt-get install -y docker-ce-cli
USER jenkins

ENTRYPOINT ["jenkins-plugin-cli"]
RUN ["--plugins", "docker-workflow"]