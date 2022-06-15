from app import app

if __name__ == '__main__':
    # path = "../app/NN_module/model/image_encoder550.pth"
    # model = torch.load(path, map_location=torch.device("cuda"))
    # input_np = np.random.uniform(0, 1, (1, 10, 32, 32))
    # input_var = Variable(torch.FloatTensor(input_np))
    # k_model = pytorch_to_keras(model, input_var, [(10, None, None,)], verbose=True)

    # models.db_setup.init_db()
    app.run(host="0.0.0.0", debug=True)
