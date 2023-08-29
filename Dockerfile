FROM python:3.9.0
ENV MPLCONFIGDIR=".config/matplotlib"
RUN mkdir -m 777 .cache .config ./flagged
RUN git clone https://github.com/szymonrucinski/AiRoll
WORKDIR /AiRoll
RUN git clone https://huggingface.co/szymonrucinski/what-a-shot
RUN ls
RUN mv ./what-a-shot ./model
RUN conda env create -f environment.yaml --quiet;
RUN pip install -r requirements.txt
RUN mkdir -m 777 flagged
EXPOSE 7860
CMD ["gradio","start_api.py"]