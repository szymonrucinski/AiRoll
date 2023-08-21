from condaforge/mambaforge

RUN git clone https://github.com/szymonrucinski/AiRoll
WORKDIR /AiRoll
RUN git clone https://huggingface.co/szymonrucinski/what-a-shot
RUN ls
RUN mv ./what-a-shot ./model
RUN conda env create -f environment.yaml
RUN conda activate airoll
CMD ["gradio", "app.py"]
EXPOSE 7860